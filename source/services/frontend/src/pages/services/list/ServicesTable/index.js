import { useSearchParams, Link } from 'react-router-dom';
import { Modal, Spin, Table, Tooltip, Dropdown, Space, Typography } from 'antd';
import qs from 'qs';
import { get } from 'lodash';
import Icon, { CopyOutlined, EllipsisOutlined } from '@ant-design/icons';
import { debounceEvent, transformDate } from '@/common/utils/helper';
import { AuthButton, Auth } from '@/common/components';
import Icons from '@/common/components/Icon';
import { ADDRESS_TYPE } from '@/common/constants';
const { Paragraph } = Typography;

const ServicesTable = ({
  tableData = {},
  loading = false,
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
      width: '10%',
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
            {icon}
            {value.desc}
          </label>
        );
      },
    },
    {
      title: '名称',
      dataIndex: 'name',
      width: '10%',
      ellipsis: {
        showTitle: false,
      },
      render(value, _) {
        return (
          <Tooltip placement="topLeft" title={value}>
            <Link to={`/services/list/detail?id=${_.id}`}>{value}</Link>
          </Tooltip>
        );
      },
    },
    {
      title: '项目',
      dataIndex: 'project',
      width: '12%',
      render(value) {
        return get(value, 'name', '-');
      },
    },
    {
      title: '镜像',
      dataIndex: 'image',
      width: '20%',
      ellipsis: {
        showTitle: false,
      },
      render(value) {
        let _value = get(value, 'name', '-');
        _value = _value?.replace(
          'swr.cn-north-4.myhuaweicloud.com/digitalbrain/',
          ''
        );
        return (
          <Tooltip placement="topLeft" title={_value}>
            {_value}
          </Tooltip>
        );
      },
    },
    {
      title: '资源',
      width: '10%',
      dataIndex: 'source',
      render(value) {
        return value || '-';
      },
    },
    {
      title: '公网访问',
      dataIndex: 'isPublic',
      width: '10%',
      render(value) {
        return value ? '是' : '否';
      },
    },
    {
      title: 'URL',
      dataIndex: 'urls',
      width: '10%',
      render(value) {
        const els = value?.map(({ type, address }, index) => (
          <Tooltip
            key={index}
            title={
              <div>
                {ADDRESS_TYPE[type]}IP:
                <Paragraph
                  style={{ color: '#fff', display: 'inline-block' }}
                  copyable={{ tooltips: false }}
                >
                  {address}
                </Paragraph>
              </div>
            }
          >
            {address}
          </Tooltip>
        ));
        return <>{[...els]}</>;
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
      title: '操作',
      width: '12%',
      // shouldCellUpdate: (record, prevRecord) =>
      //   record?.status?.desc !== prevRecord?.status?.desc,
      render(_value, record) {
        const statusName = get(record, 'status.name');
        let items = [
          {
            key: '2',
            label: (
              <AuthButton
                required="services.list.edit"
                type="text"
                onClick={() => {
                  handleDeleteClicked(record);
                }}
                condition={[
                  () => ['stopped', 'error'].indexOf(statusName) > -1,
                  (user) =>
                    get(record, 'creator.username') === get(user, 'username'),
                ]}
              >
                删除
              </AuthButton>
            ),
          },
        ];
        return (
          <Auth required="services.list.edit">
            <Space className="dbr-table-actions">
              {statusName === 'stopped' && (
                <AuthButton
                  required="services.list.edit"
                  type="link"
                  onClick={debounceEvent(() => handleStartClicked(record))}
                  condition={[
                    (user) =>
                      get(record, 'creator.username') === get(user, 'username'),
                  ]}
                >
                  启动
                </AuthButton>
              )}
              {statusName !== 'stopped' && (
                <AuthButton
                  required="services.list.edit"
                  type="link"
                  onClick={() => {
                    handleStopClicked(record);
                  }}
                  condition={[
                    () => ['error', 'stop'].indexOf(statusName) < 0,
                    (user) =>
                      get(record, 'creator.username') === get(user, 'username'),
                  ]}
                >
                  停止
                </AuthButton>
              )}
              <AuthButton
                required="services.list.edit"
                type="text"
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
              <Dropdown menu={{ items }} placement="bottom">
                <a>
                  <EllipsisOutlined style={{ fontSize: 24 }} />
                </a>
              </Dropdown>
            </Space>
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
export default ServicesTable;
