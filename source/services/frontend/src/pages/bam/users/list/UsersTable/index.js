import { useSearchParams } from 'react-router-dom';
import { Table, Button } from 'antd';
import qs from 'qs';
import { map } from 'lodash';
import { transformDate } from '@/common/utils/helper';

const UsersTable = ({
  tableData = {},
  loading = false,
  onEdit = () => {},
  onDelete = () => {},
  onPageNoChange = () => {},
}) => {
  const columns = [
    {
      title: '姓名',
      dataIndex: 'username',
    },
    {
      title: '邮箱',
      dataIndex: 'email',
    },
    {
      title: '角色',
      dataIndex: 'role',
      render(value) {
        return value.value || value;
      },
    },
    {
      title: '所属项目',
      dataIndex: 'projects',
      render(value) {
        return (value.length > 0 && map(value, 'name').join(',')) || value;
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
        const { role } = record;
        if (role.name === 'admin') {
          return;
        }
        return (
          <span className="dbr-table-actions">
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
export default UsersTable;
