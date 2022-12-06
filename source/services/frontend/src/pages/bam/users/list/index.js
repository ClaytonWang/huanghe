/**
 * @description 用户列表
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { useEffect, useState, useCallback, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Input, message, Form, Select, Modal } from 'antd';
import { filter, map } from 'lodash';
import qs from 'qs';
import { PlusOutlined, ExclamationCircleOutlined } from '@ant-design/icons';
import { parseKVToKeyValue, purifyDeep } from '@/common/utils/helper';
import { AuthButton, FormModal } from '@/common/components';
import api from '@/common/api';
import UsersTable from './UsersTable';
import { EMAIL_REG, USER_ROLE } from '@/common/constants';
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
        role__name: 'all',
        projects__code: 'all',
      },
    }),
    []
  );
  const [tableData, setTableData] = useState();
  const [projectsDataSource, setProjectsDataSource] = useState([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [initialFormValues, setInitialFormValues] = useState(null);
  const [loading, setLoading] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();

  const getFilters = useCallback(
    () => ({ ...defaultFilters, ...qs.parse(searchParams.toString()) }),
    [defaultFilters, searchParams]
  );

  const requestList = useCallback(
    async (args) => {
      const params = purifyDeep({ ...getFilters(), ...args });
      setLoading(true);
      try {
        const { result } = await api.bamUsersList(params);
        setTableData(result);
        setLoading(false);
      } catch (error) {
        console.log(error);
        setLoading(false);
      }
    },
    [getFilters]
  );
  const requestProjects = async () => {
    try {
      const { result } = await api.bamProjectsList();
      setProjectsDataSource(result.data);
    } catch (error) {
      console.log(error);
    }
  };

  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    requestList();
    requestProjects();
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
    const params = { ...values, role: values.role.name };
    try {
      await api.bamUsersCreate(params);
      message.success('用户新建成功!');
      reload();
      handleCreateCancel();
    } catch (error) {
      console.log(error);
      handleCreateCancel();
    }
  };
  const updateUser = async (values) => {
    const { id } = initialFormValues;
    const params = { ...values, role: values.role.name, userId: id };
    try {
      await api.bamUsersUpdate(params);
      message.success('用户更新成功!');
      reload();
      handleEditCancel();
    } catch (error) {
      console.log(error);
      handleEditCancel();
    }
  };
  const handleCreateClicked = () => {
    setShowCreateModal(true);
  };
  const handleCreateCancel = () => {
    setShowCreateModal(false);
  };
  const handleEditClicked = (record) => {
    setShowEditModal(true);
    const value = record.projects;
    const projects = (value.length > 0 && map(value, 'id')) || value;
    setInitialFormValues({
      ...record,
      // TODO：project字段改成projects，与列表中字段保持一致。
      project: projects,
    });
  };
  const handleEditCancel = () => {
    setShowEditModal(false);
    setInitialFormValues(null);
  };
  const handleDelete = (record) => {
    const { id } = record;
    Modal.confirm({
      title: '确定要删除该用户吗？',
      content: '将用户使用资源清空后，该用户可被删除。',
      icon: <ExclamationCircleOutlined />,
      okText: '确认',
      cancelText: '取消',
      onOk: async () => {
        try {
          await api.bamUsersDelete({ userId: id });
          message.success('用户删除成功！');
          reload();
        } catch (error) {
          console.log(error);
        }
      },
    });
  };
  const handleCreateSubmit = (values) => {
    createUser(values);
  };
  const handleEditSubmit = (values) => {
    updateUser(values);
  };
  const renderFormItems = (type) => (
    <>
      <Form.Item
        label="姓名"
        name="username"
        rules={[{ required: true, message: '请输入用户名' }]}
      >
        <Input placeholder="请输入用户名" />
      </Form.Item>
      <Form.Item
        label="邮箱"
        name="email"
        rules={[
          { required: true, message: '请输入邮箱' },
          { pattern: EMAIL_REG, message: '请输入有效邮箱' },
        ]}
      >
        <Input placeholder="请输入邮箱" disabled={type === 'edit'} />
      </Form.Item>
      <Form.Item
        label={(type === 'edit' && '新密码') || '密码'}
        name="password"
        rules={
          (type === 'edit' && [{ len: 8, message: '请输入8位密码' }]) || [
            { required: true, message: '请输入密码' },
            { len: 8, message: '请输入8位密码' },
          ]
        }
      >
        <Input.Password placeholder="请输入8位密码" />
      </Form.Item>
      <Form.Item
        name={['role', 'name']}
        label="角色"
        rules={[{ required: true, message: '请选择用户角色' }]}
      >
        <Select placeholder="请选择用户角色">
          {(type === 'create' &&
            filter(
              parseKVToKeyValue(USER_ROLE, 'k', 'v'),
              ({ k }) => k !== 'admin'
            ).map(({ k, v }) => (
              <Option key={k} value={k}>
                {v}
              </Option>
            ))) ||
            parseKVToKeyValue(USER_ROLE, 'k', 'v').map(({ k, v }) => (
              <Option key={k} value={k}>
                {v}
              </Option>
            ))}
        </Select>
      </Form.Item>
      <Form.Item name="project" label="所属项目">
        <Select mode="tags" placeholder="请选择项目">
          {projectsDataSource.map(({ id, name }) => (
            <Option key={id} value={id}>
              {name}
            </Option>
          ))}
        </Select>
      </Form.Item>
    </>
  );
  const renderCreateModal = () => (
    <FormModal
      title="新建用户"
      okText="新建"
      cancelText="取消"
      onSubmit={handleCreateSubmit}
      onCancel={handleCreateCancel}
    >
      {renderFormItems('create')}
    </FormModal>
  );

  const renderEditModal = () => (
    <FormModal
      title="编辑用户"
      okText="保存"
      cancelText="取消"
      initialValues={initialFormValues}
      onSubmit={handleEditSubmit}
      onCancel={handleEditCancel}
    >
      {renderFormItems('edit')}
    </FormModal>
  );
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
            required="bam.projects.create"
            style={{ float: 'left' }}
            type="primary"
            onClick={handleCreateClicked}
          >
            <PlusOutlined />
            新建用户
          </AuthButton>
        </div>
        <UsersTable
          tableData={tableData}
          reload={reload}
          loading={loading}
          onEdit={handleEditClicked}
          onDelete={handleDelete}
          onPageNoChange={onPageNoChange}
        />
      </div>
      {showCreateModal && renderCreateModal()}
      {showEditModal && renderEditModal()}
    </div>
  );
};
export default UsersList;
