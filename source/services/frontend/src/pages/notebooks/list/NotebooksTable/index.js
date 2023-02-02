import { useSearchParams, Link } from 'react-router-dom';
import { Modal, Spin, Table, Tooltip, Dropdown } from 'antd';
import qs from 'qs';
import { get } from 'lodash';
import Icon, { EllipsisOutlined } from '@ant-design/icons';
import { transformDate } from '@/common/utils/helper';
import { AuthButton, Auth } from '@/common/components';
import Icons from '@/common/components/Icon';
import { USER } from '@/common/constants';

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
      width: '5%',
      ellipsis: true,
      render(value) {
        let icon = (
          <Icon
            style={{ fontSize: 18, marginRight: 5 }}
            component={Icons[value.name]}
          />
        );
        if (/^(stop|start|pending)$/.test(value.name)) {
          icon = (
            <Spin
              indicator={
                <Icon
                  style={{ fontSize: 16, marginRight: 5 }}
                  component={Icons[value.name]}
                  spin
                  rotate={(/pending/.test(value.name) && 180) || 0}
                />
              }
            />
          );
        }
        return (
          <label>
            <Tooltip title={value.desc}>{icon}</Tooltip>
            {value.desc}
          </label>
        );
      },
    },
    {
      title: '名称',
      dataIndex: 'name',
      width: '10%',
      render(value, _) {
        return <Link to={`/notebooks/detail?id=${_.id}`}>{value}</Link>;
      },
    },
    {
      title: '项目',
      dataIndex: 'project',
      width: '15%',
      render(value) {
        return get(value, 'name', '-');
      },
    },
    {
      title: '镜像',
      dataIndex: 'image',
      width: '15%',
      render(value) {
        return get(value, 'name', '-');
      },
    },
    {
      title: '资源',
      width: '15%',
      dataIndex: 'source',
      render(value) {
        return get(value, 'name', '-');
      },
    },
    {
      title: '创建人',
      dataIndex: 'creator',
      width: '10%',
      render(value) {
        return get(value, 'username', '-');
      },
    },
    {
      title: '创建时间',
      dataIndex: 'createdAt',
      width: '10%',
      render(value) {
        return transformDate(value) || '-';
      },
    },
    {
      title: '操作',
      width: '15%',
      render(_value, record) {
        const statusName = get(record, 'status.name');
        let items = [
          {
            key: '1',
            label: (
              <AuthButton
                required="notebooks.list.edit"
                type="link"
                onClick={() => {
                  handleEditClicked(record);
                }}
                condition={[
                  () => ['stopped'].indexOf(statusName) > -1,
                  (user) =>
                    get(record, 'creator.username') === get(user, 'username'),
                ]}
              >
                编辑
              </AuthButton>
            ),
          },
          {
            key: '2',
            label: (
              <AuthButton
                required="notebooks.list.edit"
                type="link"
                onClick={() => {
                  handleDeleteClicked(record);
                }}
                condition={[
                  () => ['stopped', 'error'].indexOf(statusName) > -1,
                  (user) => {
                    if (user.role.name === USER) {
                      return (
                        get(record, 'creator.username') ===
                        get(user, 'username')
                      );
                    }
                    return true;
                  },
                ]}
              >
                删除
              </AuthButton>
            ),
          },
        ];
        return (
          <Auth required="notebooks.list.edit">
            <span className="dbr-table-actions">
              <AuthButton
                required="notebooks.list"
                type="link"
                onClick={() => {
                  handleOpenClicked(record);
                }}
                condition={[
                  () => ['running'].indexOf(statusName) > -1,
                  (user) => {
                    if (user.role.name === USER) {
                      return (
                        get(record, 'creator.username') ===
                        get(user, 'username')
                      );
                    }
                    return true;
                  },
                ]}
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
                  condition={[
                    (user) => {
                      if (user.role.name === USER) {
                        return (
                          get(record, 'creator.username') ===
                          get(user, 'username')
                        );
                      }
                      return true;
                    },
                  ]}
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
                  condition={[
                    () => ['error', 'stop'].indexOf(statusName) < 0,
                    (user) => {
                      if (user.role.name === USER) {
                        return (
                          get(record, 'creator.username') ===
                          get(user, 'username')
                        );
                      }
                      return true;
                    },
                  ]}
                >
                  停止
                </AuthButton>
              )}
              <Dropdown menu={{ items }}>
                <a>
                  <EllipsisOutlined />
                </a>
              </Dropdown>
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
    Modal.confirm({
      title: '可能会导致数据丢失，是否要停止该notebook服务？',
      okText: '停止',
      cancelText: '取消',
      onOk: () => {
        onStop(record);
      },
    });
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
