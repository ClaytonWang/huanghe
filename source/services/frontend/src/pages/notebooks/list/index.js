/**
 * @description 存储列表
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Modal, message } from 'antd';
import qs from 'qs';
import api from '@/common/api';
import { AuthButton } from '@/common/components';
import { purifyDeep } from '@/common/utils/helper';
import { PlusOutlined } from '@ant-design/icons';
import NotebooksFilter from './NotebooksFilter';
import NotebooksTable from './NotebooksTable';
import './index.less';
import { NOTEBOOK_ACTION, START, STOP } from '@/common/constants';

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

  const reload = (args) => {
    const filters = getFilters();
    const params = purifyDeep({ ...filters, ...args });
    // 手动同步Url
    setSearchParams(qs.stringify(params));
    requestList(params);
  };
  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    requestList();
    requestProjects();
    const filters = getFilters();
    setSearchParams(qs.stringify(filters));
  }, []);
  useEffect(() => {
    const timer = setInterval(() => {
      requestList();
    }, 3000);
    return () => {
      clearInterval(timer);
    };
  }, []);

  const onPageNoChange = (pageno, pagesize) => {
    reload({ pageno, pagesize });
  };

  const deleteNotebook = async (record) => {
    const { id } = record;
    try {
      await api.notebooksListDelete({ id });
      message.success('存储Notebook成功！');
      reload();
    } catch (error) {
      console.log(error);
    }
  };

  const handleCreateClicked = () => {
    // router to create page
  };
  const handleOpenClicked = (record) => {
    // 打开notebooks地址
    const { url } = record;
    window.open(url);
  };
  const handleStartClicked = async (record) => {
    try {
      const { id } = record;
      await api.notebooksListAction({ id, action: NOTEBOOK_ACTION[START] });
    } catch (error) {
      console.log(error);
    }
  };
  const handleStopClicked = async (record) => {
    try {
      const { id } = record;
      await api.notebooksListAction({ id, action: NOTEBOOK_ACTION[STOP] });
    } catch (error) {
      console.log(error);
    }
  };
  const handleEditClicked = () => {
    // router to create page
  };
  const handleDelete = (record) => {
    Modal.confirm({
      title: '确定要删除该Notebook吗？',
      okText: '删除',
      okType: 'danger',
      cancelText: '取消',
      onOk: () => {
        deleteNotebook(record);
      },
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
          onOpen={handleOpenClicked}
          onStart={handleStartClicked}
          onStop={handleStopClicked}
          onEdit={handleEditClicked}
          onDelete={handleDelete}
          onPageNoChange={onPageNoChange}
        />
      </div>
    </div>
  );
};
export default NotebooksList;
