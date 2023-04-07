/**
 * @description 存储列表
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { useCallback, useEffect, useMemo, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { Modal, message } from 'antd';
import qs from 'qs';
import { PlusOutlined } from '@ant-design/icons';
import api from '@/common/api';
import { AuthButton } from '@/common/components';
import { purifyDeep } from '@/common/utils/helper';
import ServicesTable from './ServicesTable';
import {
  CREATE,
  ACTION,
  START,
  STOP,
  UPDATE,
  // ADMIN,
} from '@/common/constants';
import './index.less';

const ServicesList = () => {
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
  const [loading, setLoading] = useState(false);
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
        const { result } = await api.servicesList(params);
        setTableData(result);
        setLoading(false);
      } catch (error) {
        console.log(error);
        setLoading(false);
      }
    },
    [getFilters]
  );

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

  const deleteService = async (record) => {
    const { id } = record;
    try {
      await api.servicesListDelete({ id });
      message.success('删除Service成功！');
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
    // 打开Services地址
    const { url } = record;
    window.open(url);
  };
  const handleStartClicked = async (record) => {
    try {
      const { id } = record;
      await api.servicesListAction({ id, action: ACTION[START] });
      message.success('已触发启动！');
    } catch (error) {
      console.log(error);
    }
  };
  const handleStopClicked = async (record) => {
    try {
      const { id } = record;
      await api.servicesListAction({ id, action: ACTION[STOP] });
      message.success('已触发停止！');
    } catch (error) {
      console.log(error);
    }
  };
  const handleEditClicked = (values) => {
    const { id } = values;
    navigate(`update/${id}`, {
      state: {
        params: values,
        type: UPDATE,
      },
    });
  };
  const handleDelete = (record) => {
    Modal.confirm({
      title: '确定要删除该Service吗？',
      okText: '删除',
      okType: 'danger',
      cancelText: '取消',
      onOk: () => {
        deleteService(record);
      },
    });
  };
  return (
    <div className="services-list">
      <div className="dbr-table-container">
        <div className="batch-command">
          <AuthButton
            required="deployments.list.create"
            style={{ float: 'left' }}
            type="primary"
            onClick={handleCreateClicked}
          >
            <PlusOutlined />
            新建部署
          </AuthButton>
        </div>
        <ServicesTable
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
export default ServicesList;
