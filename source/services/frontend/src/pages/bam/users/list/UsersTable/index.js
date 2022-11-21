import { useNavigate, useSearchParams } from 'react-router-dom';
import { Table, Button } from 'antd';
import qs from 'qs';
import { map } from 'lodash';
import { transformDate } from '@/common/utils/helper';
import { USER_ROLE } from '@/common/constants';

const UsersTable = ({
  tableData = {},
  loading = false,
  onEdit = () => {},
  onDelete = () => {},
  onPageNoChange = () => {},
}) => {
  // const navigate = useNavigate();
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
        return USER_ROLE[value] || value;
      },
    },
    {
      title: '所属项目',
      dataIndex: 'project',
      render(value) {
        return (value.length > 0 && map(value, 'name').join(',')) || value;
      },
    },
    {
      title: '创建时间',
      dataIndex: 'createDate',
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
  const { pageNo = 1, pageSize = 10 } = {
    ...qs.parse(searchParams.toString()),
  };

  const { totalCount = 0, data = [] } = tableData;
  const pagination = {
    current: Number(pageNo),
    pageSize: Number(pageSize),
    total: totalCount,
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
