/**
 * @description 存储列表
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Form, Input, InputNumber, message, Modal, Select } from 'antd';
import { PlusOutlined, InfoCircleOutlined } from '@ant-design/icons';
import { find, map } from 'lodash';
import { useAuth } from '@/common/hooks/useAuth';
import { ADMIN, CREATE, EDIT, OWNER, USER } from '@/common/constants';
import { AuthButton, FormModal } from '@/common/components';
import { purifyDeep, relativeDate } from '@/common/utils/helper';
import api from '@/common/api';
import qs from 'qs';
import StoragesTable from './StoragesTable';
import './index.less';

const { Option } = Select;

const StoragesList = () => {
  const defaultFilters = useMemo(
    () => ({
      pageno: 1,
      pagesize: 10,
      sort: 'id:desc',
      filter: {},
    }),
    []
  );
  const [tableData, setTableData] = useState();
  const [projectsDataSource, setProjectsDataSource] = useState([]);
  const [usersDatasource, setUsersDatasource] = useState([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [initialFormValues, setInitialFormValues] = useState(null);
  const [loading, setLoading] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();
  const { user } = useAuth();

  const getFilters = useCallback(
    () => ({ ...defaultFilters, ...qs.parse(searchParams.toString()) }),
    [defaultFilters, searchParams]
  );

  const requestList = useCallback(
    async (args) => {
      const params = purifyDeep({ ...getFilters(), ...args });
      setLoading(true);
      try {
        const { result } = await api.storagesList(params);
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
      if (user.role.name === ADMIN) {
        const { result } = await api.bamProjectsList();
        setProjectsDataSource(result.data);
      } else {
        // 项目负责任项目列表返回自己所属项目
        setProjectsDataSource(user?.projects ?? []);
      }
    } catch (error) {
      console.log(error);
    }
  };
  const requestUserListItems = async () => {
    try {
      let data = [];
      if (user.role.name === ADMIN) {
        // admin返回所有项目负责人和普通用户
        const { result = {} } = await api.userListItems();
        data = result || [];
      } else if (user.role.name === OWNER) {
        // 项目负责人，返回所有其项目下普通用户。
        const { result = {} } = await api.userListItems({
          roleName: [USER, OWNER],
          project: map(user.projects, 'id'),
        });
        data = result || [];
      } else {
        // 普通用户，所有人的用户列表只有自己。
        data = [
          {
            id: user.id,
            username: user.username,
          },
        ];
      }
      setUsersDatasource(data);
    } catch (error) {
      console.log(error);
    }
  };

  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    requestList();
    requestProjects();
    requestUserListItems();
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

  const createStorage = async (values) => {
    const params = {
      ...values,
      owner: find(usersDatasource, values.owner),
    };
    try {
      await api.storagesListCreate(params);
      message.success('存储新建成功!');
      reload();
      handleCreateCancel();
    } catch (error) {
      console.log(error);
      handleCreateCancel();
    }
  };
  const updateStorage = async (values) => {
    const { id } = initialFormValues;
    const params = {
      ...values,
      id,
      owner: find(usersDatasource, values.owner),
    };
    try {
      await api.storagesListUpdate(params);
      message.success('存储更新成功!');
      reload();
      handleEditCancel();
    } catch (error) {
      console.log(error);
      handleEditCancel();
    }
  };
  const deleteStorage = async (record) => {
    const { id } = record;
    try {
      await api.storagesListDelete({ id });
      message.success('存储删除成功！');
      reload();
    } catch (error) {
      console.log(error);
    }
  };
  const resetStorage = async (record) => {
    const { id } = record;
    try {
      await api.storagesListReset({ id });
      message.success('存储恢复成功！');
      reload();
    } catch (error) {
      console.log(error);
    }
  };
  const handleCreateClicked = () => {
    const { id, username } = user;
    const values = {
      config: { size: 1 },
      owner: { id, username },
    };
    setInitialFormValues(values);
    setShowCreateModal(true);
  };
  const handleCreateCancel = () => {
    setShowCreateModal(false);
    setInitialFormValues(null);
  };
  const handleEditClicked = (record) => {
    setShowEditModal(true);
    setInitialFormValues({
      ...record,
    });
  };
  const handleEditCancel = () => {
    setShowEditModal(false);
    setInitialFormValues(null);
  };
  const handleDelete = (record) => {
    Modal.confirm({
      title: '确定要删除该存储吗？',
      content: (
        <>
          <span>会导致全部数据丢失，是否要删除该存储？</span>
          <br />
          <span>该存储盘中没有Notebook或Job挂载可完成删除。</span>
          <br />
          <span>删除后7天之内可恢复。</span>
        </>
      ),
      okText: '删除',
      okType: 'danger',
      cancelText: '取消',
      onOk: () => {
        deleteStorage(record);
      },
    });
  };
  const handleReset = (values) => {
    const { deletedAt } = values;
    const now = new Date();
    const days = relativeDate(now, new Date(deletedAt));
    if (days > 7) {
      Modal.info({
        title: '该资源已删除超过7天，无法恢复。',
      });
    } else {
      resetStorage(values);
    }
  };
  const handleCreateSubmit = (values) => {
    createStorage(values);
  };
  const handleEditSubmit = (values) => {
    updateStorage(values);
  };
  const renderFormItems = (type) => {
    const role = user.role.name;
    // admin无最大申请空间限制
    const adminConfigRules = [
      { required: true, message: '请输入所需最大容量' },
      {
        min: 0,
        message: '请输入大于0的整数',
        type: 'number',
      },
    ];
    const defaultConfigRules = [
      { required: true, message: '请输入所需最大容量' },
      {
        min: 0,
        message: '请输入大于0的整数',
        type: 'number',
      },
      {
        max: 1024,
        message: '申请最大容量不能超过1024GB',
        type: 'number',
      },
    ];
    const isNameDisabled = () => type === EDIT;
    const isOwnerDisabled = () => user.role.name === USER;
    return (
      <>
        <Form.Item
          label="名称"
          name="name"
          rules={[
            { required: true, message: '请输入存储名称' },
            {
              pattern: /^[a-zA-Z]\w*/,
              message:
                '名字需字母开头，由字母、数字、中划线组合，长度不超过20位',
            },
            { max: 20, message: '最长不超过20字符' },
          ]}
          tooltip={{
            title: '名字需字母开头，由字母、数字、中划线组合，长度不超过20位',
            icon: <InfoCircleOutlined />,
          }}
        >
          <Input placeholder="请输入存储名称" disabled={isNameDisabled()} />
        </Form.Item>
        <Form.Item
          label="所属项目"
          name={['project', 'id']}
          rules={[{ required: true, message: '请选择所属项目' }]}
        >
          <Select placeholder="请选择所属项目">
            {projectsDataSource.map(({ id, name }) => (
              <Option key={id} value={id}>
                {name}
              </Option>
            ))}
          </Select>
        </Form.Item>
        <Form.Item label="存储配置">
          <Form.Item
            name={['config', 'size']}
            rules={(role === ADMIN && adminConfigRules) || defaultConfigRules}
            tooltip={{
              title: '可联系超级管理员扩容',
              icon: <InfoCircleOutlined />,
            }}
            noStyle
          >
            <InputNumber
              placeholder="请输入所需最大容量"
              style={{ width: '40%' }}
            />
          </Form.Item>
          <span style={{ marginLeft: 8 }}>GB</span>
        </Form.Item>
        <Form.Item
          label="所有人"
          name={['owner', 'id']}
          rules={[{ required: true, message: '请选择所有人' }]}
        >
          <Select
            placeholder="请选择所有人"
            showSearch
            filterOption={(input, option) =>
              (option?.children ?? '').includes(input)
            }
            disabled={isOwnerDisabled()}
          >
            {usersDatasource.map(({ id, username }) => (
              <Option key={id} value={id}>
                {username}
              </Option>
            ))}
          </Select>
        </Form.Item>
      </>
    );
  };
  const renderCreateModal = () => (
    <FormModal
      title="新建存储"
      okText="新建"
      cancelText="取消"
      onSubmit={handleCreateSubmit}
      onCancel={handleCreateCancel}
      initialValues={initialFormValues}
    >
      {renderFormItems(CREATE)}
    </FormModal>
  );

  const renderEditModal = () => (
    <FormModal
      title="编辑存储"
      okText="保存"
      cancelText="取消"
      initialValues={initialFormValues}
      onSubmit={handleEditSubmit}
      onCancel={handleEditCancel}
    >
      {renderFormItems(EDIT)}
    </FormModal>
  );
  return (
    <div className="storages-list">
      <div className="dbr-table-container">
        <div className="batch-command">
          <AuthButton
            required="storages.list.create"
            style={{ float: 'left' }}
            type="primary"
            onClick={handleCreateClicked}
          >
            <PlusOutlined />
            新建存储
          </AuthButton>
        </div>
        <StoragesTable
          tableData={tableData}
          reload={reload}
          loading={loading}
          onEdit={handleEditClicked}
          onDelete={handleDelete}
          onReset={handleReset}
          onPageNoChange={onPageNoChange}
        />
      </div>
      {showCreateModal && renderCreateModal()}
      {showEditModal && renderEditModal()}
    </div>
  );
};
export default StoragesList;
