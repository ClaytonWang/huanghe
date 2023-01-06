/**
 * @description 成员列表
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { Form, message, Select } from 'antd';
import { useSearchParams } from 'react-router-dom';
import qs from 'qs';
import { uniqueId, find, cloneDeep } from 'lodash';
import { PlusOutlined } from '@ant-design/icons';
import { purifyDeep } from '@/common/utils/helper';
import { useAuth } from '@/common/hooks/useAuth';
import { AuthButton, FormModal } from '@/common/components';
import { CREATE, DEFAULT_PASSWORD } from '@/common/constants';
import api from '@/common/api';
import UsersTable from './UsersTable';
import UsersFilter from './UsersFilter';
import './index.less';

const PROJECT = 'project';
const { Option } = Select;

const UsersList = () => {
  const defaultFilters = useMemo(
    () => ({
      pageno: 1,
      pagesize: 10,
      sort: 'id:desc',
      filter: {
        user__username: '',
        permissions__code: 'all',
        project__code: 'all',
      },
    }),
    []
  );
  const [tableData, setTableData] = useState({});
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [initialFormValues, setInitialFormValues] = useState(null);
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();
  const [searchParams, setSearchParams] = useSearchParams();
  const projectsDataSource = useMemo(() => user.projects || [], [user]);
  const [permissionsDatasource, setPermissionsDatasource] = useState([]);
  const [usersDatasource, setUsersDatasource] = useState([]);

  const getFilters = useCallback(
    () => ({ ...defaultFilters, ...qs.parse(searchParams.toString()) }),
    [searchParams, defaultFilters]
  );
  const requestList = useCallback(
    async (args) => {
      const params = purifyDeep({ ...cloneDeep(getFilters()), ...args });
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
    requestPermissionsDatasource();
    requestUserListItems();
    const filters = getFilters();
    setSearchParams(qs.stringify(filters));
  }, []);

  const requestPermissionsDatasource = async () => {
    try {
      // FIXME: project是后端代码逻辑，该接口给前端增加了不相干的硬编码，建议后期做优化。
      const { result } = await api.access({ name: PROJECT });
      const { children: data } = find(result, ['name', PROJECT]);
      setPermissionsDatasource(data);
    } catch (error) {
      console.log(error);
    }
  };
  const requestUserListItems = async () => {
    try {
      const { result = {} } = await api.bamUsersList({
        filter: { role__name: 'user' },
      });
      const data = result.data || [];
      setUsersDatasource(data);
    } catch (error) {
      console.log(error);
    }
  };
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
      console.log(error);
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
      setInitialFormValues({
        // FIXME：AIDP-159，hard code编辑权限，31为编辑权限id
        permissions: 31,
      });
    } else {
      setShowEditModal(true);
      setInitialFormValues({
        ...parseSeletedItem({
          ...values,
        }),
        permissions: 31,
      });
    }
  };
  const closeModal = () => {
    setShowCreateModal(false);
    setShowEditModal(false);
    setSelectedItem(null);
    setInitialFormValues(null);
  };
  // FIXME: permissions冗余的数组结构引入的「数据处理」代码，如后期无相关前端页面扩展，建议优化
  const parseSeletedItem = (record) => {
    const { permissions = [], userId } = record;
    return {
      ...record,
      permissions: permissions[0] && permissions[0].id,
      user: userId,
    };
  };
  const handleCreateClicked = () => {
    openModal('create', { password: DEFAULT_PASSWORD });
  };
  const handleCancelClicked = () => {
    closeModal();
  };
  const handleCreateSubmit = (values) => {
    const { permissions: permissionId } = values;
    createUser({ ...values, permissions: [permissionId] });
  };
  const handleEditSubmit = (values) => {
    const { userId, id } = selectedItem;
    const { permissions: permissionId, project } = values;
    updateUsers({ pk: id, user: userId, permissions: [permissionId], project });
  };
  const handleEditClicked = (record) => {
    openModal('edit', { ...record, project: record.project.id });
  };
  const handleDelete = (values) => {
    const { id } = values;
    deleteUser({ pk: id });
  };

  const renderItems = (type) => {
    let disabled = false;
    if (type === 'edit') {
      disabled = true;
    }
    return (
      <>
        <Form.Item
          name="user"
          label="姓名"
          rules={[{ required: true, message: '请选择成员' }]}
        >
          <Select
            placeholder="请选择成员"
            showSearch
            filterOption={(input, option) =>
              (option?.children ?? '').includes(input)
            }
            disabled={disabled}
          >
            {usersDatasource.map(({ id, username }) => (
              <Option key={id} value={id}>
                {username}
              </Option>
            ))}
          </Select>
        </Form.Item>
        <Form.Item
          name="project"
          label="所属项目"
          rules={[{ required: true, message: '请选择项目' }]}
        >
          <Select placeholder="请选择项目">
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
          name="permissions"
          label="权限"
          rules={[{ required: true, message: '请选择用户权限' }]}
        >
          <Select placeholder="请选择用户权限" disabled>
            {permissionsDatasource.map(({ id, value }) => (
              <Option key={id} value={id}>
                {value}
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
        permissionsDatasource={permissionsDatasource}
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
          initialValues={initialFormValues}
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
          initialValues={initialFormValues}
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
