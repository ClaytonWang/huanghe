/**
 * @description 存储列表
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Modal } from 'antd';
import qs from 'qs';
import api from '@/common/api';
import { AuthButton } from '@/common/components';
import { purifyDeep } from '@/common/utils/helper';
import { ExclamationCircleOutlined, PlusOutlined } from '@ant-design/icons';
import NotebooksFilter from './NotebooksFilter';
import NotebooksTable from './NotebooksTable';
import './index.less';

const NotebooksList = () => {
  const defaultFilters = useMemo(
    () => ({
      pageno: 1,
      pagesize: 10,
      sort: 'id:desc',
      filter: {
        name: null,
        role__name: 'all',
        project__code: 'all',
      },
    }),
    []
  );
  const [tableData, setTableData] = useState();
  const [projectsDatasource, setProjectsDatasource] = useState([]);
  // const [sourceDatasource, setSourceDatasource] = useState([]);
  // const [imagesDatasource, setImagesDatasource] = useState([]);
  // const [storagesDatasource, setStoragesDatasource] = useState([]);
  // const [initialFormValues, setInitialFormValues] = useState(null);
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
        const { result } = await api.notebooksList(params);
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
      setProjectsDatasource(result.data);
    } catch (error) {
      console.log(error);
    }
  };
  // const requestImages = async () => {
  //   try {
  //     const { result = {} } = await api.imagesList({
  //       filter: { role__name: 'user' },
  //     });
  //     const data = result.data || [];
  //     setImagesDatasource(data);
  //   } catch (error) {
  //     console.log(error);
  //   }
  // };
  const requestSource = async () => {
    try {
      const { result = {} } = await api.sourceList({
        filter: { role__name: 'user' },
      });
      const _data = result.data || [];
      // setSourceDatasource(data);
    } catch (error) {
      console.log(error);
    }
  };
  const requestStorages = async () => {
    try {
      const { result = {} } = await api.storagesList({
        filter: { role__name: 'user' },
      });
      const _data = result.data || [];
      // setStoragesDatasource(data);
    } catch (error) {
      console.log(error);
    }
  };

  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    requestList();
    requestProjects();
    requestSource();
    requestStorages();
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

  // const createNotebooks = async (_values) => {};
  // const deleteNotebook = async (record) => {
  //   const { id } = record;
  //   try {
  //     await api.storagesListDelete({ id });
  //     message.success('存储删除成功！');
  //     reload();
  //   } catch (error) {
  //     console.log(error);
  //   }
  // };

  const handleCreateClicked = () => {
    // setShowCreateModal(true);
  };

  const handleEditClicked = (_record) => {};
  // const handleCreate = () => {};
  // const handleEdit = () => {};
  // const handleOpen = () => {};
  // const handleStart = () => {};
  // const handleStop = () => {};
  const handleDelete = (_record) => {
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
      onOk: () => {},
    });
  };
  return (
    <div className="storages-list">
      <NotebooksFilter
        initialValues={getFilters().filter}
        defaultFilters={defaultFilters.filter}
        reload={reload}
        projectsDatasource={projectsDatasource}
      />
      <div className="dbr-table-container">
        <div className="batch-command">
          <AuthButton
            required="notebooks.list.create"
            style={{ float: 'left' }}
            type="primary"
            onClick={handleCreateClicked}
          >
            <PlusOutlined />
            新建Notebook
          </AuthButton>
        </div>
        <NotebooksTable
          tableData={tableData}
          reload={reload}
          loading={loading}
          onEdit={handleEditClicked}
          onDelete={handleDelete}
          onPageNoChange={onPageNoChange}
        />
      </div>
    </div>
  );
};
export default NotebooksList;
