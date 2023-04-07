/**
 * @description Jobs列表
 * @author junshi<junshi.wang@digitalbrain.cn>
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { Form, useNavigate, useSearchParams } from 'react-router-dom';
import { Modal, message, Select } from 'antd';
import qs from 'qs';
import api from '@/common/api';
import { AuthButton, FormModal } from '@/common/components';
import { purifyDeep } from '@/common/utils/helper';
import { PlusOutlined } from '@ant-design/icons';
// import JobsFilter from './JobsFilter';
import JobsTable from './JobsTable';
import {
  CREATE,
  COPY,
  JOB_ACTION,
  START,
  STOP,
  UPDATE,
} from '@/common/constants';
import './index.less';

const JobList = () => {
  const defaultFilters = useMemo(
    () => ({
      pageno: 1,
      pagesize: 10,
      sort: 'id:desc',
      filter: {
        // username: null,
        // role__name: 'all',
        // project__code: 'all',
      },
    }),
    []
  );
  const [tableData, setTableData] = useState();
  const [loading, setLoading] = useState(false);
  const [selectedRecord, setSelectedRecord] = useState({});
  const [showDebugModal, setShowDebugModal] = useState(false);

  const [searchParams, setSearchParams] = useSearchParams();
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
        const { result } = await api.jobList(params);
        setTableData(result);
        setLoading(false);
      } catch (error) {
        console.log(error);
        setLoading(false);
      }
    },
    [getFilters]
  );

  const handleDebugClicked = (record) => {
    setSelectedRecord(record);
    setShowDebugModal(true);
  };
  const handleCancelClicked = () => {
    setSelectedRecord({});
    setShowDebugModal(false);
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

  const deleteJob = async (record) => {
    const { id } = record;
    try {
      await api.jobListDelete({ id });
      message.success('删除Job服务成功！');
      reload();
    } catch (error) {
      console.log(error);
    }
  };
  const handleCreateClicked = () => {
    navigate(CREATE, {
      state: {
        type: CREATE,
      },
    });
  };
  const handleStartClicked = async (record) => {
    try {
      const { id } = record;
      await api.jobListAction({ id, action: JOB_ACTION[START] });
      message.success('已触发启动！');
      reload();
    } catch (error) {
      console.log(error);
    }
  };
  const handleStopClicked = async (record) => {
    try {
      const { id } = record;
      await api.jobListAction({ id, action: JOB_ACTION[STOP] });
      message.success('已触发停止！');
    } catch (error) {
      console.log(error);
    }
  };
  const handleEditClicked = (values) => {
    const { id } = values;
    navigate(`${UPDATE}/${id}`, {
      state: {
        params: values,
        type: UPDATE,
      },
    });
  };
  const handleCopyClicked = (values) => {
    navigate(COPY, {
      state: {
        params: values,
        type: COPY,
      },
    });
  };
  const handleDelete = (record) => {
    Modal.confirm({
      title: '确定要删除该Job服务吗？',
      okText: '删除',
      okType: 'danger',
      cancelText: '取消',
      onOk: () => {
        deleteJob(record);
      },
    });
  };
  const DebugModal = ({ record, open, onClose }) => {
    const { url: urls = [] } = record;
    const onSubmit = ({ url }) => {
      window.open(url);
      onClose();
    };
    return (
      <FormModal
        title="个人信息"
        okText="打开"
        open={open}
        cancelText="取消"
        onSubmit={onSubmit}
        onCancel={onClose}
      >
        <Form.Item name="url">
          <Select>
            {urls.map(({ name, value }, index) => (
              <Select.Option key={index} value={value}>
                {name}
              </Select.Option>
            ))}
          </Select>
        </Form.Item>
      </FormModal>
    );
  };
  return (
    <div className="storages-list">
      {/* <JobsFilter
        initialValues={getFilters().filter}
        defaultFilters={defaultFilters.filter}
        reload={reload}
        projectsDatasource={projectsDatasource}
      /> */}
      <div className="dbr-table-container">
        <div className="batch-command">
          <AuthButton
            required="jobs.list.create"
            style={{ float: 'left' }}
            type="primary"
            onClick={handleCreateClicked}
          >
            <PlusOutlined />
            新建
          </AuthButton>
        </div>
        <JobsTable
          tableData={tableData}
          reload={reload}
          loading={loading}
          onDebug={handleDebugClicked}
          onStart={handleStartClicked}
          onStop={handleStopClicked}
          onEdit={handleEditClicked}
          onCopy={handleCopyClicked}
          onDelete={handleDelete}
          onPageNoChange={onPageNoChange}
        />
      </div>
      <DebugModal
        record={selectedRecord}
        open={showDebugModal}
        onClose={handleCancelClicked}
      />
    </div>
  );
};
export default JobList;
