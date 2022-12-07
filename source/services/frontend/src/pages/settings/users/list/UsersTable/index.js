import { useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Table, Modal } from 'antd';
import qs from 'qs';
import { ExclamationCircleOutlined } from '@ant-design/icons';
import { AuthButton } from '@/common/components';

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
      title: '所属项目',
      dataIndex: 'project',
      render(value) {
        return value.name || value;
      },
    },
    {
      title: '权限',
      dataIndex: 'permissions',
      render(arr) {
        const { value = '-' } = arr[0] || {};
        return value;
      },
    },
    {
      title: '操作',
      render(_value, record) {
        return (
          <span className="dbr-table-actions">
            <AuthButton
              type="link"
              required="settings.users.edit"
              onClick={() => {
                handleEditClicked(record);
              }}
            >
              编辑
            </AuthButton>
            <AuthButton
              type="link"
              required="settings.users.edit"
              onClick={() => {
                handleRemove(record);
              }}
            >
              移除
            </AuthButton>
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
  const genTableData = useCallback(
    (data) =>
      // 没有id，以序号生成id
      data.map((item, index) => ({ id: index, ...item })),
    []
  );

  const handleEditClicked = (data = {}) => {
    onEdit(data);
  };

  const handleRemove = (record) => {
    Modal.confirm({
      title: '确定要移除该用户吗？',
      icon: <ExclamationCircleOutlined />,
      okText: '确认',
      cancelText: '取消',
      onOk: async () => {
        onDelete(record);
      },
    });
  };

  return (
    <Table
      className="dbr-table"
      rowKey="id"
      size="middle"
      loading={loading}
      columns={columns}
      dataSource={genTableData(data)}
      pagination={pagination}
    />
  );
};
export default UsersTable;
