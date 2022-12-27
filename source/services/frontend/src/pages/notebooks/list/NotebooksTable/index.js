import { useSearchParams } from 'react-router-dom';
import { Table, Tooltip } from 'antd';
import qs from 'qs';
import { get } from 'lodash';
import Icon from '@ant-design/icons';
import { transformDate } from '@/common/utils/helper';
import { AuthButton, Auth } from '@/common/components';
import Icons from '@/common/components/Icon';

const NotebooksTable = ({
  tableData = {},
  loading = false,
  onOpen = () => {},
  onStart = () => {},
  onStop = () => {},
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
        return (
          <Tooltip title={value.desc}>
            <Icon style={{ fontSize: 24 }} component={Icons[value.name]} />
          </Tooltip>
        );
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
        const statusName = get(record, 'status.name');
        return (
          <Auth required="notebooks.list.edit">
            <span className="dbr-table-actions">
              <AuthButton
                required="notebooks.list"
                type="link"
                onClick={() => {
                  handleOpenClicked(record);
                }}
                condition={() => ['running'].indexOf(statusName) > -1}
              >
                打开
              </AuthButton>
              {statusName === 'stopped' && (
                <AuthButton
                  required="notebooks.list.edit"
                  type="link"
                  onClick={() => {
                    handleStartClicked(record);
                  }}
                >
                  启动
                </AuthButton>
              )}
              {statusName !== 'stopped' && (
                <AuthButton
                  required="notebooks.list.edit"
                  type="link"
                  onClick={() => {
                    handleStopClicked(record);
                  }}
                >
                  停止
                </AuthButton>
              )}
              <AuthButton
                required="notebooks.list.edit"
                type="link"
                onClick={() => {
                  handleEditClicked(record);
                }}
                condition={() => ['stopped'].indexOf(statusName) > -1}
              >
                编辑
              </AuthButton>
              <AuthButton
                required="notebooks.list.edit"
                type="link"
                onClick={() => {
                  handleDeleteClicked(record);
                }}
                condition={() => ['stopped'].indexOf(statusName) > -1}
              >
                删除
              </AuthButton>
            </span>
          </Auth>
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
  const handleOpenClicked = (record) => {
    onOpen(record);
  };
  const handleStartClicked = (record) => {
    onStart(record);
  };
  const handleStopClicked = (record) => {
    onStop(record);
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
