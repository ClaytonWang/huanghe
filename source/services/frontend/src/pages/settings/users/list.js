/**
 * @description 成员列表
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { Form, Input, message, Select, TreeSelect } from 'antd';
import { get } from 'lodash';
import { useSearchParams } from 'react-router-dom';
import qs from 'qs';
import { PlusOutlined } from '@ant-design/icons';
import { useAuth } from '@/common/hooks/useAuth';
import { AuthButton, FormModal } from '@/common/components';
import { useSystem } from '@/common/hooks/useSystem';
import {
  CREATE,
  DEFAULT_PASSWORD,
  EMAIL_REG,
  ROLE_MAP,
} from '@/common/constants';
import api from '@/common/api';
import { tranverseTree, tranverseTree2 } from '@/common/utils/helper';
import UsersTable from './UsersTable';

const { Option } = Select;
const UsersList = () => {
  const defaultFilters = useMemo(
    () => ({
      pageNo: 1,
      pageSize: 10,
    }),
    []
  );
  const [tableData, setTableData] = useState({});
  const [treeSelectDataSource, setTreeSelectDataSource] = useState([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [selectedItem, setSelectedItem] = useState(null);
  const [loading, setLoading] = useState(false);
  const { user } = useAuth();
  const { organizations: cachedOrganizations, loadOrganizations } = useSystem();
  const [searchParams, setSearchParams] = useSearchParams();
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
  const requestOrganizations = useCallback(async () => {
    try {
      let root = null;
      let organizations = cachedOrganizations;
      // TODO: enable tranversTree to suspend
      // TODO: orgainzation cached could remove
      if (!cachedOrganizations.length) {
        organizations = await loadOrganizations();
      }
      // TODO: refactor
      tranverseTree(organizations, (item) => {
        const orgainizationId = get(user, 'organization.id');
        if (item.id === orgainizationId) {
          root = item;
          return;
        }
      });
      let result = [];
      if (root) {
        result = tranverseTree2([root], [], (item) => {
          const { name, id } = item;
          return { title: name, value: id };
        });
      }
      setTreeSelectDataSource(result);
    } catch (error) {
      console.log(error);
    }
  }, [cachedOrganizations, loadOrganizations, user]);
  const syncSearchParams = useCallback(() => {
    const filters = getFilters();
    setSearchParams(qs.stringify(filters));
  }, [getFilters, setSearchParams]);

  useEffect(() => {
    requestList();
    requestOrganizations();
    syncSearchParams();
  }, [requestList, requestOrganizations, syncSearchParams]);

  const reload = (args) => {
    const filters = getFilters();
    const params = { ...filters, ...args };
    // 手动同步Url
    setSearchParams(params);
    requestList(params);
  };
  const onPageNoChange = (pageNo, pageSize) => {
    reload({ pageNo, pageSize });
  };
  const createUser = async (values) => {
    try {
      await api.settingsUsersCreate({ ...values });
      message.success('新成员增加成功！');
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
  const handleCreateUser = (values) => {
    const result = {
      ...values,
      organizationId: values.organization,
    };
    createUser(result);
  };
  const handleSubmit = (values) => {
    const result = {
      ...values,
      organizationId: values.organization,
      userId: selectedItem.id,
    };
    updateUsers(result);
  };
  const handleEditClicked = (record) => {
    openModal('edit', record);
  };

  const renderItems = () => (
    <>
      <Form.Item
        name="userName"
        label="姓名"
        rules={[{ required: true, message: '请输入计划名称' }]}
      >
        <Input placeholder="请输入姓名" />
      </Form.Item>
      <Form.Item
        name="role"
        label="角色"
        rules={[{ required: true, message: '请选择角色' }]}
      >
        <Select style={{ width: '100%' }} placeholder="请选择角色">
          {Object.entries(ROLE_MAP).map(([value, name], index) => (
            <Option key={index} value={value}>
              {name}
            </Option>
          ))}
        </Select>
      </Form.Item>
      <Form.Item
        name="organization"
        label="组织"
        rules={[{ required: true, message: '请选择组织' }]}
      >
        <TreeSelect
          style={{ width: '100%' }}
          placeholder="请选择组织"
          treeDefaultExpandAll
          treeData={treeSelectDataSource}
        />
      </Form.Item>
    </>
  );
  const renderCreateItems = () => (
    <>
      <Form.Item
        name="email"
        label="邮箱"
        rules={[
          { required: true, message: '请输入邮箱' },
          { pattern: EMAIL_REG, message: '请输入有效邮箱' },
        ]}
      >
        <Input placeholder="请输入邮箱" />
      </Form.Item>
      <Form.Item name="password" label="初始密码">
        <Input value={DEFAULT_PASSWORD} disabled />
      </Form.Item>
    </>
  );
  const renderEditItems = () => (
    <Form.Item name="email" label="邮箱">
      <Input disabled />
    </Form.Item>
  );

  return (
    <div className="dbr-table-container">
      <div className="batch-command">
        <AuthButton
          required="settings.users.edit"
          style={{ float: 'left' }}
          type="primary"
          onClick={handleCreateClicked}
        >
          <PlusOutlined />
          新增成员
        </AuthButton>
      </div>
      <UsersTable
        tableData={tableData}
        loading={loading}
        onEdit={handleEditClicked}
        onPageNoChange={onPageNoChange}
      />
      {showCreateModal && (
        <FormModal
          title="添加成员"
          okText="确认"
          initialValues={selectedItem}
          onSubmit={handleCreateUser}
          onCancel={handleCancelClicked}
        >
          {renderItems()}
          {renderCreateItems()}
        </FormModal>
      )}
      {showEditModal && (
        <FormModal
          title="编辑成员"
          okText="保存"
          initialValues={{
            ...selectedItem,
          }}
          onSubmit={handleSubmit}
          onCancel={handleCancelClicked}
        >
          {renderItems()}
          {renderEditItems()}
        </FormModal>
      )}
    </div>
  );
};
export default UsersList;
