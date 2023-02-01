/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-02-01 18:13:47
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-01 18:32:52
 * @FilePath: /huanghe/source/services/frontend/src/common/components/EventMonitor/index.js
 * @Description: 事件监控
 */
import { useSearchParams } from 'react-router-dom';
import qs from 'qs';
import { get } from 'lodash';
import { Table } from 'antd';
import { transformDate } from '@/common/utils/helper';

const EventMonitor = ({
  tableData = {},
  loading = false,
  onPageNoChange = () => {},
}) => {
  const columns = [
    {
      title: '状态',
      dataIndex: 'status',
      width: '10%',
      ellipsis: true,
      render(value) {
        return <label>{value}</label>;
      },
    },
    {
      title: '事件',
      dataIndex: 'event',
      width: '40%',
      render(value) {
        return get(value, 'name', '-');
      },
    },
    {
      title: '时间',
      dataIndex: 'time',
      width: '40%',
      render(value) {
        return transformDate(value) || '-';
      },
    },
  ];
  const genTableData = (data) => data;
  const [searchParams] = useSearchParams();
  const { pageno = 1, pagesize = 10 } = {
    ...qs.parse(searchParams.toString()),
  };
  const { total = 0, data = [] } = tableData;
  const pagination = {
    current: Number(pageno),
    pageSize: Number(pagesize),
    total,
    onChange: onPageNoChange,
    showSizeChanger: false,
  };
  return (
    <Table
      className="dbr-table"
      rowKey="id"
      size="small"
      columns={columns}
      loading={loading}
      dataSource={genTableData(data)}
      pagination={pagination}
    />
  );
};

export default EventMonitor;
