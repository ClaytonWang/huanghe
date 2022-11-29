/**
 * @description 成员列表
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { Form, Input, message, Select } from 'antd';
import { useSearchParams } from 'react-router-dom';
import qs from 'qs';
import { uniqueId } from 'lodash';
import { PlusOutlined } from '@ant-design/icons';
import { useAuth } from '@/common/hooks/useAuth';
import { AuthButton, FormModal } from '@/common/components';
import { ACCESS_MAP, CREATE, DEFAULT_PASSWORD } from '@/common/constants';
import api from '@/common/api';
import { parseKVToKeyValue, purifyDeep } from '@/common/utils/helper';
import UsersTable from './UsersTable';
import UsersFilter from './UsersFilter';
import './index.less';

const { Option } = Select;
const UsersList = () => {
  const defaultFilters = useMemo(
    () => ({
      pageno: 1,
      pagesize: 10,
      sort: 'id:desc',
      filter: {
        username: '',
        access: 'all',
        project: 'all',
      },
    }),
    []
  );
  const [tableData, setTableData] = useState({});
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();
  const [searchParams, setSearchParams] = useSearchParams();
  const projectsDataSource = useMemo(() => user.project || [], [user]);
  const getFilters = useCallback(
    () => ({ ...defaultFilters, ...qs.parse(searchParams.toString()) }),
    [searchParams, defaultFilters]
  );
  const requestList = useCallback(
    async (args) => {
      const params = { ...getFilters(), ...args };
      setLoading(true);
      try {
        const { result } = await api.settingsUsersList(params);
        setTableData(result);
        setLoading(false);
      } catch (error) {
        console.log(error);
        setLoading(false);
      }
    },
    [getFilters]
  );

  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    requestList();
    const filters = getFilters();
    setSearchParams(qs.stringify(filters));
  }, []);

  const reload = (args) => {
    const filters = getFilters();
    const params = purifyDeep({ ...filters, ...args });
    // 手动同步Url
    setSearchParams(qs.stringify(params));
    requestList(params);
  };
  const onPageNoChange = (pageno, pagesize) => {
    reload({ pageno, pagesize });
  };
  const createUser = async (values) => {
    try {
      await api.settingsUsersCreate({ ...values });
      message.success('添加成功！');
      closeModal();
      reload();
    } catch (error) {
      message.info(error);
    }
  };
  const updateUsers = async (values) => {
    try {
      await api.settingsUsersUpdate(values);
      message.success('编辑成功！');
      closeModal();
      reload();
    } catch (error) {
      console.log(error);
    }
  };
  const deleteUser = async (values) => {
    try {
      await api.settingsUsersDelete(values);
      message.success('用户移除成功！');
      reload();
    } catch (error) {
      console.log(error);
    }
  };
  const openModal = (type, values) => {
    if (values) {
      setSelectedItem(values);
    }
    if (type === CREATE) {
      setShowCreateModal(true);
    } else {
      setShowEditModal(true);
    }
  };
  const closeModal = () => {
    setShowCreateModal(false);
    setShowEditModal(false);
    setSelectedItem(null);
  };
  const handleCreateClicked = () => {
    openModal('create', { password: DEFAULT_PASSWORD });
  };
  const handleCancelClicked = () => {
    closeModal();
  };
  const handleCreateSubmit = (values) => {
    createUser(values);
  };
  const handleEditSubmit = (values) => {
    const { id } = selectedItem;
    updateUsers({ ...values, id });
  };
  const handleEditClicked = (record) => {
    openModal('edit', { ...record, project: record.project.id });
  };
  const handleDelete = (record) => {
    const { id = '' } = record;
    deleteUser({ id });
  };

  const renderItems = (type) => {
    let disabled = false;
    if (type === 'edit') {
      disabled = true;
    }
    return (
      <>
        <Form.Item
          name="username"
          label="姓名"
          rules={[{ required: true, message: '请输入计划名称' }]}
        >
          <Input placeholder="请输入姓名" disabled={disabled} />
        </Form.Item>
        <Form.Item
          name="project"
          label="所属项目"
          rules={[{ required: true, message: '请选择角色' }]}
        >
          <Select placeholder="请选择角色">
            {projectsDataSource.map(
              ({ id = uniqueId('settings.projectId'), name = '-' }) => (
                <Option key={id} value={id}>
                  {name}
                </Option>
              )
            )}
          </Select>
        </Form.Item>
        <Form.Item
          name="access"
          label="权限"
          rules={[{ required: true, message: '请选择用户权限' }]}
        >
          <Select placeholder="请选择用户权限">
            {parseKVToKeyValue(ACCESS_MAP, 'k', 'v').map(({ k, v }) => (
              <Option key={k} value={k}>
                {v}
              </Option>
            ))}
          </Select>
        </Form.Item>
      </>
    );
  };

  return (
    <div className="users-list">
      <UsersFilter
        initialValues={getFilters().filter}
        defaultFilters={defaultFilters.filter}
        reload={reload}
        projectsDataSource={projectsDataSource}
      />
      <div className="dbr-table-container">
        <div className="batch-command">
          <AuthButton
            required="settings.users.edit"
            style={{ float: 'left' }}
            type="primary"
            onClick={handleCreateClicked}
          >
            <PlusOutlined />
            添加成员
          </AuthButton>
        </div>
        <UsersTable
          tableData={tableData}
          loading={loading}
          onEdit={handleEditClicked}
          onDelete={handleDelete}
          onPageNoChange={onPageNoChange}
        />
      </div>
      {showCreateModal && (
        <FormModal
          title="添加成员"
          okText="确认"
          initialValues={selectedItem}
          onSubmit={handleCreateSubmit}
          onCancel={handleCancelClicked}
        >
          {renderItems('create')}
        </FormModal>
      )}
      {showEditModal && (
        <FormModal
          title="编辑成员"
          okText="保存"
          initialValues={{
            ...selectedItem,
          }}
          onSubmit={handleEditSubmit}
          onCancel={handleCancelClicked}
        >
          {renderItems('edit')}
        </FormModal>
      )}
    </div>
  );
};
export default UsersList;
