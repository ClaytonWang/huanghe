import { useSearchParams, Link } from 'react-router-dom';
import { Modal, Spin, Table, Tooltip, Dropdown, Space } from 'antd';
import qs from 'qs';
import { get } from 'lodash';
import Icon, { EllipsisOutlined } from '@ant-design/icons';
import {
  transformDate,
  getStatusName,
  debounceEvent,
} from '@/common/utils/helper';
import { Auth } from '@/common/components';
import {
  StartStopBtn,
  DeleteBtn,
  EditBtn,
  CopyBtn,
  DebugBtn,
} from '../../components';
import Icons from '@/common/components/Icon';
import { DEBUG } from '@/common/constants';

const JobsTable = ({
  tableData = {},
  loading = false,
  onStart = () => {},
  onStop = () => {},
  onEdit = () => {},
  onCopy = () => {},
  onDelete = () => {},
  onDebug = () => {},
  onPageNoChange = () => {},
}) => {
  const columns = [
    {
      title: '状态',
      dataIndex: 'status',
      width: '10%',
      render(value) {
        const status = getStatusName(value.name);
        let icon = (
          <Icon
            style={{ fontSize: 18, marginRight: 5 }}
            component={Icons[status]}
          />
        );
        if (/^(stop|start|pending)$/.test(status)) {
          icon = (
            <Spin
              indicator={
                <Icon
                  style={{ fontSize: 16, marginRight: 5 }}
                  component={Icons[status]}
                  spin
                  rotate={(/pending/.test(status) && 180) || 0}
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
      render(value, _) {
        return <Link to={`/jobs/list/detail/${_.id}`}>{value}</Link>;
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
      title: '任务模式',
      dataIndex: 'mode',
      width: '10%',
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
      shouldCellUpdate: (record, prevRecord) =>
        record?.status?.desc !== prevRecord?.status?.desc,
      render(_value, record) {
        return <OperationBtnGroup record={record} />;
      },
    },
  ];
  const OperationBtnGroup = ({ record }) => {
    const mode = get(record, 'mode');

    let items = [
      {
        key: 'copy',
        label: <CopyBtn record={record} onCopy={() => onCopy(record)} />,
      },
      {
        key: 'delete',
        label: <DeleteBtn record={record} onDelete={() => onDelete(record)} />,
      },
    ];

    if (mode === DEBUG) {
      items.unshift({
        key: 'edit',
        label: (
          <EditBtn type="text" onEdit={() => onEdit(record)} record={record} />
        ),
      });
    }

    return (
      <Auth required="jobs.list.edit">
        <span className="dbr-table-actions">
          <Space>
            <StartStopBtn
              onStart={debounceEvent(() => onStart(record))}
              onStop={() => handleStopClicked(record)}
              record={record}
            />
            {mode === DEBUG ? (
              <DebugBtn onDebug={() => onDebug(record)} record={record} />
            ) : (
              <EditBtn onEdit={() => onEdit(record)} record={record} />
            )}
            <Dropdown menu={{ items }} placement="bottom">
              <a>
                <EllipsisOutlined style={{ fontSize: 24 }} />
              </a>
            </Dropdown>
          </Space>
        </span>
      </Auth>
    );
  };

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
  const handleStopClicked = (record) => {
    Modal.confirm({
      title: '可能会导致数据丢失，是否要停止该Job服务？',
      okText: '停止',
      cancelText: '取消',
      onOk: () => {
        onStop(record);
      },
    });
  };

  return (
    <Table
      className="dbr-table"
      rowKey="id"
      size="small"
      columns={columns}
      loading={loading}
      dataSource={data}
      pagination={pagination}
    />
  );
};
export default JobsTable;
