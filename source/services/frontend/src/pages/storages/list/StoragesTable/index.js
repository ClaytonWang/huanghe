import { useSearchParams } from 'react-router-dom';
import { Table, Button } from 'antd';
import qs from 'qs';
import { get } from 'lodash';
import { transformDate } from '@/common/utils/helper';
import { AuthButton } from '@/common/components';
import { USER } from '@/common/constants';

const StoragesTable = ({
  tableData = {},
  loading = false,
  onEdit = () => {},
  onDelete = () => {},
  onReset = () => {},
  onPageNoChange = () => {},
}) => {
  const columns = [
    {
      title: '名称',
      dataIndex: 'name',
    },
    {
      title: '配置',
      dataIndex: 'config',
      render(config = {}) {
        const { size = 0 } = config;
        return `${size}GB`;
      },
    },
    {
      title: '所有人',
      dataIndex: 'owner',
      render(owner = {}) {
        return owner.username || '-';
      },
    },
    {
      title: '创建人',
      dataIndex: 'creator',
      render(creator = {}) {
        return creator.username || '-';
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
        const { deletedAt = null } = record;
        if (deletedAt) {
          return (
            <span className="dbr-table-actions">
              <Button
                type="link"
                onClick={() => {
                  handleEditClicked(record);
                }}
                disabled
              >
                编辑
              </Button>
              <Button
                type="link"
                onClick={() => {
                  handleResetClicked(record);
                }}
              >
                恢复
              </Button>
            </span>
          );
        }
        return (
          <span className="dbr-table-actions">
            <AuthButton
              type="link"
              onClick={() => {
                handleEditClicked(record);
              }}
              condition={[
                (user) => {
                  if (user.role.name === USER) {
                    return (
                      get(record, 'owner.username') === get(user, 'username')
                    );
                  }
                  return true;
                },
              ]}
            >
              编辑
            </AuthButton>
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
  const handleResetClicked = (record) => {
    onReset(record);
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
      tableLayout="auto"
    />
  );
};
export default StoragesTable;
