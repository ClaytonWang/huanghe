/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-02-01 18:13:47
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-08 10:27:00
 * @FilePath: /huanghe/source/services/frontend/src/common/components/EventMonitor/index.js
 * @Description: 事件监控
 */
import { useSearchParams } from 'react-router-dom';
import qs from 'qs';
import { Table } from 'antd';
import { transformTime } from '@/common/utils/helper';

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
      render(_, record) {
        return record?.status?.desc || '-';
      },
    },
    {
      title: '事件',
      dataIndex: 'name',
      width: '40%',
    },
    {
      title: '时间',
      dataIndex: 'time',
      width: '40%',
      render(value) {
        return transformTime(value, 'YYYY-MM-DD HH:mm:ss') || '-';
      },
    },
  ];
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
    showSizeChanger: true,
  };
  const genTableData = (data) => data;
  return (
    <Table
      className="dbr-table"
      style={{ marginTop: -10 }}
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
