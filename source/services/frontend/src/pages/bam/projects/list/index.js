/**
 * @description 数据列表页
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { useEffect, useState, useCallback, useMemo } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Input, message, Form, Select, Modal } from 'antd';
import qs from 'qs';
import { PlusOutlined, ExclamationCircleOutlined } from '@ant-design/icons';
import { AuthButton, FormModal } from '@/common/components';
import api from '@/common/api';
import ProjectsTable from './ProjectsTable';

const { Option } = Select;

const ProjectsList = () => {
  const defaultFilters = useMemo(
    () => ({
      pageno: 1,
      pagesize: 10,
      order: 'desc',
      orderBy: 'createTime',
    }),
    []
  );
  const [tableData, setTableData] = useState();
  const [ownersDatasource, setOwnersDatasource] = useState([]);
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
      const params = { ...getFilters(), ...args };
      setLoading(true);
      try {
        const { result } = await api.bamProjectsList(params);
        setTableData(result);
        setLoading(false);
      } catch (error) {
        console.log(error);
        setLoading(false);
      }
    },
    [getFilters]
  );
  const requestOwnersDatasource = async () => {
    try {
      const { result } = await api.bamUsersList({
        filter: { role__name: 'owner' },
      });
      setOwnersDatasource(result.data);
    } catch (error) {
      console.log(error);
    }
  };

  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    requestList();
    requestOwnersDatasource();
    const filters = getFilters();
    setSearchParams(qs.stringify(filters));
  }, []);

  const reload = (args) => {
    const filters = getFilters();
    const params = { ...filters, ...args };
    // 手动同步Url
    setSearchParams(params);
    requestList(params);
  };
  const onPageNoChange = (pageno, pagesize) => {
    reload({ pageno, pagesize });
  };

  const createProject = async (values) => {
    const params = { ...values, owner: values.owner.id };
    try {
      await api.bamProjectsCreate(params);
      message.success('项目新建成功！');
      setShowCreateModal(false);
      reload();
    } catch (error) {
      console.log(error);
      setShowCreateModal(false);
    }
  };
  const updateProject = async (values) => {
    const params = { ...values, owner: values.owner.id };
    try {
      await api.bamProjectsUpdate(params);
      message.success('项目修改成功！');
      handleEditModalCancel();
      reload();
    } catch (error) {
      console.log(error);
      handleEditModalCancel();
    }
  };

  const handleCreateClicked = () => {
    setShowCreateModal(true);
  };
  const handleCreateModalCancel = () => {
    setShowCreateModal(false);
  };
  const handleEdit = (record) => {
    setShowEditModal(true);
    setInitialFormValues(record);
  };
  const handleEditModalCancel = () => {
    setShowEditModal(false);
    setInitialFormValues(null);
  };
  const handleCreateSubmit = (values) => {
    createProject(values);
  };
  const handleEditSubmit = (values) => {
    const { id } = initialFormValues;
    updateProject({ projectId: id, ...values });
  };
  const handleDelete = (record) => {
    const { id } = record;
    Modal.confirm({
      title: '确定要删除该项目吗？',
      content: '将项目中的成员移除且占用资源清空后，可删除该项目。',
      icon: <ExclamationCircleOutlined />,
      okText: '确认',
      cancelText: '取消',
      onOk: async () => {
        try {
          await api.bamProjectsDelete({ projectId: id });
          message.success('项目删除成功！');
          reload();
        } catch (error) {
          console.log(error);
        }
      },
    });
  };

  const renderCreateModal = () => (
    <FormModal
      title="新建项目"
      okText="新建"
      cancelText="取消"
      onSubmit={handleCreateSubmit}
      onCancel={handleCreateModalCancel}
    >
      <Form.Item
        label="项目编号"
        name="code"
        rules={[{ required: true, message: '请输入项目编号' }]}
      >
        <Input placeholder="请输入项目编号" />
      </Form.Item>
      <Form.Item
        label="项目名称"
        name="name"
        rules={[{ required: true, message: '请输入项目名称' }]}
      >
        <Input placeholder="请输入项目名称" />
      </Form.Item>
      <Form.Item
        label="项目负责人"
        name={['owner', 'id']}
        rules={[{ required: true, message: '请选择项目负责人' }]}
      >
        <Select placeholder="请选择项目负责人">
          {ownersDatasource.map(({ id, username }) => (
            <Option key={id} value={id}>
              {username}
            </Option>
          ))}
        </Select>
      </Form.Item>
    </FormModal>
  );
  const renderEditModal = () => (
    <FormModal
      title="编辑项目"
      okText="保存"
      cancelText="取消"
      initialValues={initialFormValues}
      onSubmit={handleEditSubmit}
      onCancel={handleEditModalCancel}
    >
      <Form.Item
        label="项目编号"
        name="code"
        rules={[{ required: true, message: '请输入项目编号' }]}
      >
        <Input placeholder="请输入项目编号" />
      </Form.Item>
      <Form.Item
        label="项目名称"
        name="name"
        rules={[{ required: true, message: '请输入项目名称' }]}
      >
        <Input placeholder="请输入项目名称" />
      </Form.Item>
      <Form.Item
        label="项目负责人"
        name={['owner', 'id']}
        rules={[{ required: true, message: '请选择项目负责人' }]}
      >
        <Select placeholder="请选择项目负责人">
          {ownersDatasource.map(({ id, username }) => (
            <Option key={id} value={id}>
              {username}
            </Option>
          ))}
        </Select>
      </Form.Item>
    </FormModal>
  );

  return (
    <div className="dbr-table-container">
      <div className="batch-command">
        <AuthButton
          required="bam.projects.create"
          style={{ float: 'left' }}
          type="primary"
          onClick={handleCreateClicked}
        >
          <PlusOutlined />
          新建项目
        </AuthButton>
      </div>
      <ProjectsTable
        tableData={tableData}
        reload={reload}
        loading={loading}
        onPageNoChange={onPageNoChange}
        onDelete={handleDelete}
        onEdit={handleEdit}
      />
      {showCreateModal && renderCreateModal()}
      {showEditModal && renderEditModal()}
    </div>
  );
};
export default ProjectsList;
