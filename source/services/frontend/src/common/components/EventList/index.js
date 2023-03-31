/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-02-01 18:13:47
 * @LastEditors: guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime: 2023-03-29 11:59:01
 * @FilePath: /huanghe/source/services/frontend/src/common/components/EventList/index.js
 * @Description: 事件监控
 */
import { Table } from 'antd';
import { transformTime } from '@/common/utils/helper';

const EventList = ({
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
  const { total = 0, data = [], pageno, pagesize } = tableData;
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

export default EventList;
