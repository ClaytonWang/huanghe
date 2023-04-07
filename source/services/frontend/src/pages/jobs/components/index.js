import { get } from 'lodash';
import { getStatusName } from '@/common/utils/helper';
import { AuthButton } from '@/common/components';

const StartStopBtn = ({ record, onStart, onStop }) => {
  const _sname = get(record, 'status.name');
  const statusName = getStatusName(_sname);

  if (
    statusName === 'stopped' ||
    _sname === 'run_fail' ||
    _sname === 'start_fail'
  ) {
    return (
      <AuthButton
        required="jobs.list.edit"
        type="link"
        // onClick={debounceEvent(() => handleStartClicked(record))}
        onClick={onStart}
        condition={[
          (user) => get(record, 'creator.username') === get(user, 'username'),
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
        // onClick={() => {
        //   handleStopClicked(record);
        // }}
        onClick={onStop}
        condition={[
          () => ['stop_fail', 'stop', 'completed'].indexOf(statusName) < 0,
          (user) => get(record, 'creator.username') === get(user, 'username'),
        ]}
      >
        停止
      </AuthButton>
    );
  }
};

const DebugBtn = ({ record, onDebug }) => {
  const _sname = get(record, 'status.name');
  const statusName = getStatusName(_sname);
  const mode = get(record, 'mode');
  return (
    <AuthButton
      required="jobs.list"
      type="text"
      // onClick={() => {
      //   handleOpenClicked(record);
      // }}
      onClick={onDebug}
      condition={[
        () => ['running'].indexOf(statusName) > -1,
        (user) => get(record, 'creator.username') === get(user, 'username'),
      ]}
    >
      {mode}
    </AuthButton>
  );
};

const CopyBtn = ({ record, onCopy }) => {
  const _sname = get(record, 'status.name');
  const statusName = getStatusName(_sname);
  return (
    <AuthButton
      required="jobs.list.edit"
      type="text"
      // onClick={() => {
      //   handleCopyClicked(record);
      // }}
      onClick={onCopy}
      condition={[
        () => ['error', 'stopped', 'completed'].indexOf(statusName) > -1,
        () => ['stop_fail'].indexOf(_sname) < 0,
        (user) => get(record, 'creator.username') === get(user, 'username'),
      ]}
    >
      复制
    </AuthButton>
  );
};

const EditBtn = (props = {}) => {
  const { record, onEdit } = props;
  const _sname = get(record, 'status.name');
  const statusName = getStatusName(_sname);
  return (
    <AuthButton
      required="jobs.list.edit"
      type="link"
      {...props}
      // onClick={() => {
      //   handleEditClicked(record);
      // }}
      onClick={onEdit}
      condition={[
        () => ['error', 'stopped', 'completed'].indexOf(statusName) > -1,
        () => ['stop_fail'].indexOf(_sname) < 0,
        (user) => get(record, 'creator.username') === get(user, 'username'),
      ]}
    >
      编辑
    </AuthButton>
  );
};

const DeleteBtn = ({ record, onDelete }) => {
  const _sname = get(record, 'status.name');
  const statusName = getStatusName(_sname);
  return (
    <AuthButton
      required="jobs.list.edit"
      type="text"
      // onClick={() => {
      //   handleDeleteClicked(record);
      // }}
      onClick={onDelete}
      condition={[
        () => ['stopped', 'error', 'completed'].indexOf(statusName) > -1,
        () => ['stop_fail'].indexOf(_sname) < 0,
        (user) => get(record, 'creator.username') === get(user, 'username'),
      ]}
    >
      删除
    </AuthButton>
  );
};
export { StartStopBtn, DeleteBtn, EditBtn, CopyBtn, DebugBtn };
