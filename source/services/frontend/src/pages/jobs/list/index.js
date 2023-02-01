/**
 * @description Jobs列表
 * @author junshi<junshi.wang@digitalbrain.cn>
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Modal, message } from 'antd';
import qs from 'qs';
import api from '@/common/api';
import { AuthButton } from '@/common/components';
import { purifyDeep } from '@/common/utils/helper';
import { PlusOutlined } from '@ant-design/icons';
import JobsFilter from './JobsFilter';
import JobsTable from './JobsTable';
import {
  CREATE,
  JOB_ACTION,
  START,
  STOP,
  UPDATE,
  ADMIN,
} from '@/common/constants';
import './index.less';
import { useAuth } from '@/common/hooks/useAuth';

const JobList = () => {
  const defaultFilters = useMemo(
    () => ({
      pageno: 1,
      pagesize: 10,
      sort: 'id:desc',
      filter: {
        username: null,
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
  const { user } = useAuth();
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
  const requestProjects = async () => {
    try {
      if (user.role.name === ADMIN) {
        const { result } = await api.bamProjectsList();
        setProjectsDatasource(result.data);
      } else {
        // 除超级管理员角色，其他项目列表返回自己所属项目
        setProjectsDatasource(user?.projects ?? []);
      }
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
    requestList({ loading: true });
    requestProjects();
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
      message.success('删除Job成功！');
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
    // 打开jobs地址
    const { url } = record;
    window.open(url);
  };
  const handleStartClicked = async (record) => {
    try {
      const { id } = record;
      await api.notebooksListAction({ id, action: JOB_ACTION[START] });
      message.success('已触发启动！');
    } catch (error) {
      console.log(error);
    }
  };
  const handleStopClicked = async (record) => {
    try {
      const { id } = record;
      await api.notebooksListAction({ id, action: JOB_ACTION[STOP] });
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
      title: '确定要删除该Job吗？',
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
      <JobsFilter
        initialValues={getFilters().filter}
        defaultFilters={defaultFilters.filter}
        reload={reload}
        projectsDatasource={projectsDatasource}
      />
      <div className="dbr-table-container">
        <div className="batch-command">
          <AuthButton
            required="jobs.list.create"
            style={{ float: 'left' }}
            type="primary"
            onClick={handleCreateClicked}
          >
            <PlusOutlined />
            新建Job
          </AuthButton>
        </div>
        <JobsTable
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
export default JobList;
