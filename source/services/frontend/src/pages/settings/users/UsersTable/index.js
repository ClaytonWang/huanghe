import { useCallback } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Table, Modal, message } from 'antd';
import qs from 'qs';
import { ExclamationCircleOutlined } from '@ant-design/icons';
import { ROLE_MAP } from '@/common/constants';
import { AuthButton } from '@/common/components';
import api from '@/common/api';

const UsersTable = ({
  tableData = {},
  loading = false,
  onEdit = () => {},
  onPageNoChange = () => {},
}) => {
  const columns = [
    {
      title: '姓名',
      dataIndex: 'userName',
    },
    {
      title: '角色',
      dataIndex: 'role',
      render(value) {
        return ROLE_MAP[value] || '-';
      },
    },
    {
      title: '组织',
      dataIndex: 'organization',
      render(value) {
        return (value && value.name) || '-';
      },
    },
    {
      title: '邮箱',
      dataIndex: 'email',
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
                handleResetPwdClicked(record);
              }}
            >
              重置密码
            </AuthButton>
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
  const genTableData = useCallback(
    (data) =>
      // 没有id，以序号生成id
      data.map((item, index) => ({ id: index, ...item })),
    []
  );

  const handleEditClicked = (data = {}) => {
    onEdit(data);
  };

  const handleResetPwdClicked = (record) => {
    Modal.confirm({
      title: '确定要重置该用户密码吗？',
      icon: <ExclamationCircleOutlined />,
      okText: '确认',
      cancelText: '取消',
      onOk: async () => {
        try {
          const { id: userId } = record;
          await api.settingsUsersPasswordReset({ userId });
          message.success('密码重置成功！');
        } catch (error) {
          console.log(error);
        }
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
