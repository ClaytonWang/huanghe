/**
 * @description 存储列表
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { get } from 'lodash';
import qs from 'qs';
import { Form, Input, InputNumber, message, Modal, Select } from 'antd';
import { ExclamationCircleOutlined, PlusOutlined } from '@ant-design/icons';
import api from '@/common/api';
import { Auth, AuthButton, FormModal } from '@/common/components';
import { purifyDeep, relativeDate } from '@/common/utils/helper';
import { useAuth } from '@/common/hooks/useAuth';
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
      const { result } = await api.bamProjectsList();
      setProjectsDataSource(result.data);
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

  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    requestList();
    requestProjects();
    if (user.role.name === 'admin') {
      requestUserListItems();
    }
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
      config: get(values, 'config.size'),
      project: get(values, 'project.id'),
      owner: get(values, 'owner.id'),
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
      config: get(values, 'config.size'),
      project: get(values, 'project.id'),
      owner: get(values, 'owner.id'),
      id,
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
    setShowCreateModal(true);
  };
  const handleCreateCancel = () => {
    setShowCreateModal(false);
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
      title: '确定要删除该用户吗？',
      content: (
        <>
          <span>会导致全部数据丢失，是否要删除该存储？</span>
          <br />
          <span>该存储盘中没有Notebook或Job挂载可完成删除。</span>
          <br />
          <span>删除后7天之内可恢复。</span>
        </>
      ),
      icon: <ExclamationCircleOutlined />,
      okText: '确认',
      cancelText: '取消',
      onOk: () => {
        deleteStorage(record);
      },
    });
  };
  const handleReset = (values) => {
    const { deleteTime } = values;
    const now = new Date();
    const days = relativeDate(now, new Date(deleteTime));
    if (days > 7) {
      Modal.info({
        title: '该资源已删除超过7天，无法恢复。',
      });
    } else {
      Modal.confirm({
        title: '恢复',
        icon: <ExclamationCircleOutlined />,
        content: (
          <>
            <span>会导致全部数据丢失，是否要删除该存储？</span>
            <br />
            <span>该存储盘中没有Notebook或Job挂载可完成删除。</span>
            <br />
            <span>删除后7天之内可恢复。</span>
          </>
        ),
        okText: '确认',
        cancelText: '取消',
        onOk: () => {
          resetStorage(values);
        },
      });
    }
  };
  const handleCreateSubmit = (values) => {
    createStorage(values);
  };
  const handleEditSubmit = (values) => {
    updateStorage(values);
  };
  const renderFormItems = () => (
    <>
      <Form.Item
        label="名称"
        name="name"
        rules={[
          { required: true, message: '请输入存储名' },
          { pattern: /^\w+/, message: '请输入英文名称' },
        ]}
      >
        <Input placeholder="请输入存储名" />
      </Form.Item>
      <Form.Item
        name={['project', 'id']}
        label="所属项目"
        rules={[{ required: true, message: '请输入所属项目' }]}
      >
        <Select placeholder="请选择项目">
          {projectsDataSource.map(({ id, name }) => (
            <Option key={id} value={id}>
              {name}
            </Option>
          ))}
        </Select>
      </Form.Item>
      <Form.Item
        label="配置"
        name={['config', 'size']}
        rules={[
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
        ]}
      >
        <InputNumber
          placeholder="请输入所需最大容量"
          formatter={(value) => `${value} GB`}
          parser={(value) => value && value.replace('GB', '')}
          style={{ width: '30%' }}
        />
      </Form.Item>
      <Auth condition={(user) => user.role.name === 'admin'}>
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
          >
            {usersDatasource.map(({ id, username }) => (
              <Option key={id} value={id}>
                {username}
              </Option>
            ))}
          </Select>
        </Form.Item>
      </Auth>
    </>
  );
  const renderCreateModal = () => (
    <FormModal
      title="新建存储"
      okText="新建"
      cancelText="取消"
      onSubmit={handleCreateSubmit}
      onCancel={handleCreateCancel}
      initialValues={{ config: { size: 0 } }}
    >
      {renderFormItems('create')}
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
      {renderFormItems('edit')}
    </FormModal>
  );
  return (
    <div className="storages-list">
      <div className="dbr-table-container">
        <div className="batch-command">
          <AuthButton
            required="bam.projects.create"
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
