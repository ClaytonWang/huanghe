/**
 * @description 存储列表
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Modal, message } from 'antd';
import qs from 'qs';
import api from '@/common/api';
import { AuthButton } from '@/common/components';
import { purifyDeep } from '@/common/utils/helper';
import { PlusOutlined } from '@ant-design/icons';
// import NotebooksFilter from './NotebooksFilter';
import NotebooksTable from './NotebooksTable';
import {
  CREATE,
  NOTEBOOK_ACTION,
  START,
  STOP,
  UPDATE,
  // ADMIN,
} from '@/common/constants';
import './index.less';
// import { useAuth } from '@/common/hooks/useAuth';

const NotebooksList = () => {
  const defaultFilters = useMemo(
    () => ({
      pageno: 1,
      pagesize: 10,
      sort: 'update_at:desc',
      filter: {
        username: null,
        role__name: 'all',
        project__code: 'all',
      },
    }),
    []
  );
  const [tableData, setTableData] = useState();
  // const [projectsDatasource, setProjectsDatasource] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchParams, setSearchParams] = useSearchParams();
  // const { user } = useAuth();
  const navigate = useNavigate();

  const getFilters = useCallback(
    () => ({ ...defaultFilters, ...qs.parse(searchParams.toString()) }),
    [defaultFilters, searchParams]
  );

  const requestList = useCallback(
    async (args) => {
      const { loading = false, ...rest } = args;
      const params = purifyDeep({ ...getFilters(), ...rest });
      try {
        setLoading(loading);
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
  // const requestProjects = async () => {
  //   try {
  //     if (user.role.name === ADMIN) {
  //       const { result } = await api.bamProjectsList();
  //       setProjectsDatasource(result.data);
  //     } else {
  //       // 除超级管理员角色，其他项目列表返回自己所属项目
  //       setProjectsDatasource(user?.projects ?? []);
  //     }
  //   } catch (error) {
  //     console.log(error);
  //   }
  // };

  const reload = (args) => {
    const filters = getFilters();
    const params = purifyDeep({ ...filters, ...args });
    // 手动同步Url
    setSearchParams(qs.stringify(params));
    requestList(params);
  };
  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    requestList({ loading: true });
    // requestProjects();
    const filters = getFilters();
    setSearchParams(qs.stringify(filters));
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      reload();
    }, 3000);
    return () => {
      clearInterval(timer);
    };
  }, [searchParams]);

  const onPageNoChange = (pageno, pagesize) => {
    reload({ pageno, pagesize });
  };

  const deleteNotebook = async (record) => {
    const { id } = record;
    try {
      await api.notebooksListDelete({ id });
      message.success('删除Notebook成功！');
      reload();
    } catch (error) {
      console.log(error);
    }
  };

  const handleCreateClicked = () => {
    navigate('create', {
      state: {
        type: CREATE,
      },
    });
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
      message.success('已触发启动！');
    } catch (error) {
      console.log(error);
    }
  };
  const handleStopClicked = async (record) => {
    try {
      const { id } = record;
      await api.notebooksListAction({ id, action: NOTEBOOK_ACTION[STOP] });
      message.success('已触发停止！');
    } catch (error) {
      console.log(error);
    }
  };
  const handleEditClicked = (values) => {
    navigate('update', {
      state: {
        params: values,
        type: UPDATE,
      },
    });
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
      {/* <NotebooksFilter
        initialValues={getFilters().filter}
        defaultFilters={defaultFilters.filter}
        reload={reload}
        projectsDatasource={projectsDatasource}
      /> */}
      <div className="dbr-table-container">
        <div className="batch-command">
          <AuthButton
            required="notebooks.list.create"
            style={{ float: 'left' }}
            type="primary"
            onClick={handleCreateClicked}
          >
            <PlusOutlined />
            新建
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
