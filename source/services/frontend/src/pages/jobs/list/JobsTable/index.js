import { useSearchParams, Link } from 'react-router-dom';
import { Modal, Spin, Table, Tooltip, Dropdown, Space } from 'antd';
import qs from 'qs';
import { get } from 'lodash';
import Icon, { EllipsisOutlined } from '@ant-design/icons';
import { transformDate, getStatusName } from '@/common/utils/helper';
import { AuthButton, Auth } from '@/common/components';
import Icons from '@/common/components/Icon';
import { DEBUG } from '@/common/constants';

const JobsTable = ({
  tableData = {},
  loading = false,
  onOpen = () => {},
  onStart = () => {},
  onStop = () => {},
  onEdit = () => {},
  onCopy = () => {},
  onDelete = () => {},
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
        if (/^(stop|start|pending|running)$/.test(status)) {
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
        return <Link to={`/jobs/list/detail?id=${_.id}`}>{value}</Link>;
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
        const _value = get(value, 'name', '-');
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
      width: '10%',
      shouldCellUpdate: (record, prevRecord) =>
        record?.status?.desc !== prevRecord?.status?.desc,
      render(_value, record) {
        return <OperationBtnGroup record={record} />;
      },
    },
  ];
  const OperationBtnGroup = ({ record }) => {
    const _sname = get(record, 'status.name');
    const statusName = getStatusName(_sname);
    const taskModel = get(record, 'taskModel_name');

    const StartStopBtn = () => {
      if (
        statusName === 'stopped' ||
        _sname === 'run_fail' ||
        _sname === 'start_fail'
      ) {
        return (
          <AuthButton
            required="jobs.list.edit"
            type="link"
            onClick={() => {
              handleStartClicked(record);
            }}
            condition={[
              (user) =>
                get(record, 'creator.username') === get(user, 'username'),
            ]}
          >
            启动
          </AuthButton>
        );
      }
      if (statusName !== 'stopped') {
        return (
          <AuthButton
            required="jobs.list.edit"
            type="link"
            onClick={() => {
              handleStopClicked(record);
            }}
            condition={[
              () => ['stop_fail', 'stop', 'completed'].indexOf(statusName) < 0,
              (user) =>
                get(record, 'creator.username') === get(user, 'username'),
            ]}
          >
            停止
          </AuthButton>
        );
      }
    };

    const DebugBtn = () => (
      <AuthButton
        required="jobs.list"
        type="link"
        onClick={() => {
          handleOpenClicked(record);
        }}
        condition={[
          () => ['running'].indexOf(statusName) > -1,
          (user) => get(record, 'creator.username') === get(user, 'username'),
        ]}
      >
        {taskModel}
      </AuthButton>
    );

    const CopyBtn = () => (
      <AuthButton
        required="jobs.list.edit"
        type="link"
        onClick={() => {
          handleCopyClicked(record);
        }}
        condition={[
          () => ['error', 'stopped', 'completed'].indexOf(statusName) > -1,
          () => ['stop_fail'].indexOf(_sname) < 0,
          (user) => get(record, 'creator.username') === get(user, 'username'),
        ]}
      >
        复制
      </AuthButton>
    );

    const EditBtn = () => (
      <AuthButton
        required="jobs.list.edit"
        type="link"
        onClick={() => {
          handleEditClicked(record);
        }}
        condition={[
          () => ['stopped', 'completed'].indexOf(statusName) > -1,
          (user) => get(record, 'creator.username') === get(user, 'username'),
        ]}
      >
        编辑
      </AuthButton>
    );

    const DeleteBtn = () => (
      <AuthButton
        required="jobs.list.edit"
        type="link"
        onClick={() => {
          handleDeleteClicked(record);
        }}
        condition={[
          () => ['stopped', 'error', 'completed'].indexOf(statusName) > -1,
          () => ['stop_fail'].indexOf(_sname) < 0,
          (user) => get(record, 'creator.username') === get(user, 'username'),
        ]}
      >
        删除
      </AuthButton>
    );
    let items = [
      {
        key: 'copy',
        label: <CopyBtn />,
      },
      {
        key: 'delete',
        label: <DeleteBtn />,
      },
    ];

    if (taskModel === DEBUG) {
      items.unshift({
        key: 'edit',
        label: <EditBtn />,
      });
    }

    return (
      <Auth required="jobs.list.edit">
        <span className="dbr-table-actions">
          <Space>
            <StartStopBtn />
            {taskModel === DEBUG ? <DebugBtn /> : <EditBtn />}
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
  const handleOpenClicked = (record) => {
    onOpen(record);
  };
  const handleStartClicked = (record) => {
    onStart(record);
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
  const handleEditClicked = (record) => {
    onEdit(record);
  };
  const handleCopyClicked = (record) => {
    onCopy(record);
  };
  const handleDeleteClicked = (record) => {
    onDelete(record);
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
