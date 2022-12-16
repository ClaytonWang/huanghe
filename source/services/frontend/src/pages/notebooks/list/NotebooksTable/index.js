import { useSearchParams } from 'react-router-dom';
import { Table, Button } from 'antd';
import qs from 'qs';
import { transformDate } from '@/common/utils/helper';

const NotebooksTable = ({
  tableData = {},
  loading = false,
  onEdit = () => {},
  onDelete = () => {},
  onPageNoChange = () => {},
}) => {
  const columns = [
    {
      title: '状态',
      dataIndex: 'status',
      width: 80,
      render(value) {
        return value.name;
      },
    },
    {
      title: '名称',
      dataIndex: 'name',
      width: 120,
    },
    {
      title: '项目',
      dataIndex: 'project',
      width: 180,
      render(value) {
        return value.name || value;
      },
    },
    {
      title: '镜像',
      dataIndex: 'image',
      width: 180,
      render(value) {
        return value.name || value;
      },
    },
    {
      title: '资源',
      dataIndex: 'source',
      width: 180,
    },
    {
      title: '创建人',
      dataIndex: 'creator',
      render(value) {
        return value.username || '-';
      },
    },
    {
      title: '创建时间',
      dataIndex: 'createdAt',
      render(value) {
        return transformDate(value) || '-';
      },
    },
    {
      title: '操作',
      render(_value, record) {
        return (
          <span className="dbr-table-actions">
            <Button
              type="link"
              onClick={() => {
                handleEditClicked(record);
              }}
            >
              打开
            </Button>
            <Button
              type="link"
              onClick={() => {
                handleEditClicked(record);
              }}
            >
              启动/停止
            </Button>
            <Button
              type="link"
              onClick={() => {
                handleEditClicked(record);
              }}
            >
              编辑
            </Button>
            <Button
              type="link"
              onClick={() => {
                handleDeleteClicked(record);
              }}
            >
              删除
            </Button>
          </span>
        );
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
    showSizeChanger: false,
  };
  const handleEditClicked = (record) => {
    onEdit(record);
  };
  const handleDeleteClicked = (record) => {
    onDelete(record);
  };
  const genTableData = (data) => data;

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
export default NotebooksTable;
