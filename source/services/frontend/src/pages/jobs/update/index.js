/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-12-22 10:48:26
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-23 09:40:59
 * @Description Job 新建/编辑页
 */
import { useEffect, useState, useMemo, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Button,
  Divider,
  Form,
  Input,
  message,
  Select,
  Tooltip,
  Checkbox,
  Space,
} from 'antd';
import { uniqueId, get, map, drop } from 'lodash';
import {
  DeleteFilled,
  InfoCircleOutlined,
  PlusOutlined,
} from '@ant-design/icons';
import api from '@/common/api';
import { CREATE, UPDATE, COPY, ADMIN } from '@/common/constants';
import { useContextProps } from '@/common/hooks/RoutesProvider';
import { useAuth } from '@/common/hooks/useAuth';
import { genUniqueIdByPrefix, ID } from '@/common/utils/helper';
import { AuthButton } from '@/common/components';
import './index.less';

const { Option } = Select;
const { TextArea } = Input;

const taskModes = [
  { id: 0, name: '调试' },
  { id: 1, name: '非调试' },
];

const JobsUpdate = () => {
  const [projectsDatasource, setProjectsDatasource] = useState([]);
  const [imagesDatasource, setImagesDatasource] = useState([]);
  const [sourceDatasource, setSourceDatasource] = useState([]);
  const [storagesDatasource, setStoragesDatasource] = useState([]);
  const [selectedStorages, setSelectedStorages] = useState([]);
  const [taskMode, setTaskMode] = useState(taskModes[0].name);
  const setContextProps = useContextProps();
  const [type, setType] = useState(CREATE);
  const uniqueID = useRef();
  const { user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [form] = Form.useForm();

  const updateSelectedStorage = (values, transform) => {
    let result = [];
    if (transform) {
      result = transform(values);
    } else {
      result = map(get(values, 'hooks', []), 'storage').map(({ id }) => id);
    }
    setSelectedStorages([...result]);
  };

  const requestJob = async (params) => {
    try {
      const { result } = await api.jobDetail({ ...params });
      populateDetail(result);
    } catch (error) {
      console.log(error);
    }
  };

  const populateDetail = (detail) => {
    const _detail = {
      ...detail,
      id: type === COPY ? null : detail?.id,
      name: type === COPY ? `${detail?.name}-1` : detail?.name,
    };
    setTaskMode(_detail.mode);
    form.setFieldsValue(_detail);
    updateSelectedStorage(_detail);
  };

  const requestProjects = async () => {
    try {
      if (user.role.name === ADMIN) {
        const { result } = await api.bamProjectsList();
        setProjectsDatasource(result.data);
      } else {
        // 除超级管理员角色，其他项目列表返回自己所属项目
        setProjectsDatasource(user?.projects ?? []);
      }
    } catch (error) {
      console.log(error);
    }
  };

  const projectDefaultValue = useMemo(() => {
    if (projectsDatasource && projectsDatasource.length > 0) {
      return {
        name: projectsDatasource[0]?.name,
        id: projectsDatasource[0]?.id,
      };
    }
  }, [projectsDatasource]);

  const requestImages = async () => {
    try {
      const { result } = await api.jobImageList();
      setImagesDatasource(result.data);
    } catch (error) {
      console.log(error);
    }
  };

  const imageDefaultValue = useMemo(() => {
    if (imagesDatasource && imagesDatasource.length > 0) {
      return {
        custom: false,
        id: imagesDatasource[0]?.id,
        name: imagesDatasource[0]?.name,
      };
    }
  }, [imagesDatasource]);

  const requestSource = async () => {
    try {
      const { result } = await api.jobSourceList();
      setSourceDatasource(result.data);
    } catch (error) {
      console.log(error);
    }
  };
  const requestStorages = async () => {
    try {
      const { result } = await api.storagesList({
        filter: { isdeleted: false },
      });
      setStoragesDatasource(
        result.data.map(({ id, ...rest }) => ({ id: Number(id), ...rest }))
      );
    } catch (error) {
      console.log(error);
    }
  };
  const saveJob = async (values) => {
    try {
      await api.jobListCreate(values);
      message.success('创建成功！');
      backToList();
    } catch (error) {
      console.log(error);
    }
  };
  const updateJob = async (values) => {
    try {
      await api.jobListUpdate(values);
      message.success('保存成功!');
      backToList();
    } catch (error) {
      console.log(error);
    }
  };

  const backToList = () => {
    navigate('/jobs/list', { state: null });
  };
  const updateStorage = (changedFields, allFields) => {
    const changedStorage = changedFields.find((field) =>
      /hooks,[0-9]+,storage/.test(field.name.toString())
    );
    const changedHooks = changedFields.find((field) =>
      /^hooks$/.test(field.name.toString())
    );
    // 新增挂载，并选择存储，更新selectedStorage集合
    if (changedStorage) {
      updateSelectedStorage(allFields, (values) =>
        values
          .filter((field) => /hooks,[0-9]+,storage/.test(field.name.toString()))
          .map(({ value = null }) => value || false)
          .filter((value) => value)
      );
    } else if (changedHooks) {
      // 删除/新增挂载，通过hooks下的value数组，更新selectedStorage集合
      updateSelectedStorage(get(changedHooks, 'value', []), (values) =>
        values
          .map(({ storage }) => storage?.id || false)
          .filter((value) => value)
      );
    }
  };
  const handleSubmit = () => {
    const values = form.getFieldsValue();
    const { id = null } = get(location, 'state.params', {});
    console.log(values);
    if (type === CREATE || type === COPY) {
      saveJob(values);
    } else {
      updateJob({ id, ...values });
    }
  };
  const handleSubmitFailed = ({ errorFields }) => {
    message.error(errorFields[0].errors[0]);
    console.log(errorFields);
  };
  const handleCancelClicked = () => {
    backToList();
  };
  const handleFieldsChange = (changedFields, allFields) => {
    updateStorage(changedFields, allFields);
    return changedFields;
  };
  const handleCreateStorageClicked = () => {
    navigate('/storages/list', {
      state: {
        params: { showCreateModal: true },
      },
    });
  };

  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    requestProjects();
    requestImages();
    requestSource();
    requestStorages();
    uniqueID.current = new ID();
    setContextProps({
      onCancel: handleCancelClicked,
      onSubmit: () => {
        form.submit();
      },
    });
  }, []);

  useEffect(() => {
    const { id = null } = get(location, 'state.params', {});
    const type = get(location, 'state.type');
    if (type === UPDATE || type === COPY) {
      requestJob({ id });
    } else {
      form.setFieldsValue({
        project: projectDefaultValue,
        image: imageDefaultValue,
        mode: taskMode,
      });
    }
    setType(type);
  }, [location, form, projectDefaultValue, imageDefaultValue]);

  const HooksItem = ({ name, remove, selectedStorages, disabledItems }) => {
    const currStorage = form.getFieldValue(['hooks', name, 'storage', 'id']);
    const filteredStorageOptions = useMemo(() => {
      const result = storagesDatasource.filter(
        // 非选中了的存储集合的元素及当前选择的存储元素的集合
        ({ id }) => !(selectedStorages.includes(id) && id !== currStorage)
      );
      return result;
    }, [selectedStorages, storagesDatasource]);
    return (
      <>
        <div className="notebooks-hooks-item">
          <span className="content">
            <Form.Item
              name={[name, 'storage', 'id']}
              label="存储盘"
              rules={[{ required: true, message: '请选择存储盘' }]}
            >
              <Select
                placeholder="请选择存储盘"
                showSearch
                filterOption={(input, option) =>
                  (option?.children ?? '').includes(input)
                }
                options={filteredStorageOptions.map(
                  ({ id, name = '-', config, creator }) => ({
                    label: (
                      <>
                        <Tooltip title={name}>{name}</Tooltip>
                        <span
                          style={{ color: '#bfbfbf', float: 'right' }}
                        >{`${config.size}G`}</span>
                        <span
                          style={{
                            color: '#bfbfbf',
                            float: 'right',
                            marginRight: 8,
                          }}
                        >{`${(creator && creator.username) || '-'}创建`}</span>
                      </>
                    ),
                    value: id,
                  })
                )}
                notFoundContent={
                  <div className="select-notfound">
                    <span>暂无存储盘</span>,
                    <AuthButton
                      required="storages.list.create"
                      type="link"
                      onClick={handleCreateStorageClicked}
                    >
                      点击新建
                    </AuthButton>
                  </div>
                }
              />
            </Form.Item>
            <Form.Item
              name={[name, 'path']}
              label="目录"
              rules={[{ required: true, message: '请输入存储目录' }]}
            >
              <Input
                placeholder="请输入目录"
                disabled={disabledItems && disabledItems.includes('path')}
              />
            </Form.Item>
          </span>
          {remove && (
            <span className="action">
              <DeleteFilled onClick={() => remove(name)} />
            </span>
          )}
        </div>
        <Divider />
      </>
    );
  };

  const checkImage = (_, value) => {
    if (value?.name) {
      return Promise.resolve();
    }
    return Promise.reject(new Error('请输入镜像！'));
  };

  const CustomImage = ({ value, onChange }) => {
    const [custom, setCustom] = useState(value?.custom);
    const onCheckChange = (e) => {
      setCustom(e.target.checked);
      onChange?.({
        custom: e.target.checked,
        name: null,
      });
    };
    const onInputChange = (e) => {
      onChange?.({ custom: true, name: e.target.value });
    };
    const onSelectChange = (value) => {
      onChange?.({ custom: false, name: value });
    };
    return (
      <>
        {custom ? (
          <Input
            placeholder="输入镜像地址"
            onChange={onInputChange}
            value={value?.name}
          />
        ) : (
          <Select
            placeholder="请选择镜像"
            showSearch
            filterOption={(input, option) =>
              (option?.value ?? '').includes(input)
            }
            defaultValue={value?.name}
            onChange={onSelectChange}
          >
            {imagesDatasource.map(({ id, name, desc }) => (
              <Option key={id} value={name}>
                <Tooltip
                  title={
                    <div>
                      <p>镜像名称: {name}</p>
                      <p>说明: {desc}</p>
                    </div>
                  }
                >
                  {name}
                </Tooltip>
              </Option>
            ))}
          </Select>
        )}

        <Checkbox checked={custom} onChange={onCheckChange}>
          自定义镜像
          <Tooltip title="请填写公共镜像仓库，如：tensorflow:1.13">
            <InfoCircleOutlined style={{ marginLeft: 5, cursor: 'help' }} />
          </Tooltip>
        </Checkbox>
      </>
    );
  };
  const ProjectSelect = ({ value, onChange }) => {
    const onSelectChange = (value) => {
      onChange?.({ id: value });
    };
    return (
      <Select
        placeholder="请选择项目"
        defaultValue={value?.id}
        onChange={onSelectChange}
      >
        {projectsDatasource.map(({ id, name = '-' }) => (
          <Option key={id} value={id}>
            {name}
          </Option>
        ))}
      </Select>
    );
  };

  const JobModel = ({ value, onChange }) => {
    const onSelectChange = (value) => {
      onChange?.(value);
      setTaskMode(value);
    };
    return (
      <Select
        placeholder="请选择任务模式"
        defaultValue={value || taskModes[0].name}
        onChange={onSelectChange}
      >
        {taskModes.map(({ id, name = '-' }) => (
          <Option key={id} value={name}>
            {name}
          </Option>
        ))}
      </Select>
    );
  };
  return (
    <div className="notebooks-update">
      <Form
        className="notebooks-update-form"
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        onFinishFailed={handleSubmitFailed}
        onCancel={handleCancelClicked}
        onFieldsChange={handleFieldsChange}
      >
        <Form.Item
          name="name"
          label="名称"
          rules={[
            { required: true, message: '请输入Job名称' },
            {
              pattern: /^[a-zA-z][0-9a-zA-Z-]*$/,
              message: '字母开头，可以是字母、数字、中划线组合',
            },
            { max: 20, message: '长度不超过20字符' },
          ]}
          tooltip={{
            title: '字母开头，可以是字母、数字、中划线组合',
            icon: <InfoCircleOutlined />,
          }}
        >
          <Input placeholder="请输入Job名称" disabled={type === UPDATE} />
        </Form.Item>
        <Form.Item
          name="project"
          label="项目"
          rules={[{ required: true, message: '请选择项目' }]}
        >
          <ProjectSelect />
        </Form.Item>
        <Form.List name="hooks">
          {(fields = [], { add, remove }, { errors }) => (
            <>
              <Form.Item label="存储挂载" wrapperCol={{ push: 2, xs: 22 }}>
                {selectedStorages.length > 0 && (
                  <HooksItem
                    key={uniqueId('hook-')}
                    {...fields[0]}
                    selectedStorages={selectedStorages}
                    disabledItems={['path']}
                  />
                )}
                {drop([...fields], selectedStorages.length > 0 ? 1 : 0).map(
                  (field) => (
                    <HooksItem
                      key={uniqueId('hook-')}
                      {...field}
                      remove={remove}
                      selectedStorages={selectedStorages}
                    />
                  )
                )}
                <Button
                  style={{ width: '100%' }}
                  onClick={() =>
                    add({
                      path: `/home/jovyan/${genUniqueIdByPrefix(
                        'vol-',
                        uniqueID.current
                      )}`,
                    })
                  }
                >
                  <PlusOutlined />
                  添加
                </Button>
                <Form.ErrorList errors={errors} />
              </Form.Item>
            </>
          )}
        </Form.List>
        <Form.Item
          name="mode"
          label="模式"
          rules={[{ required: true, message: '请选择模式' }]}
        >
          <JobModel />
        </Form.Item>
        {taskMode !== taskModes[0].name && (
          <Form.Item
            name="startCommand"
            label="启动命令"
            tooltip={{
              title: '...',
              icon: <InfoCircleOutlined />,
            }}
            rules={[{ required: true, message: '请输入启动命令' }]}
          >
            <TextArea rows={4} placeholder="输入..." />
          </Form.Item>
        )}

        <Form.Item
          name="image"
          label="镜像"
          rules={[
            { required: true, message: '请选择镜像' },
            {
              validator: checkImage,
            },
          ]}
        >
          <CustomImage />
        </Form.Item>
        <Form.Item
          name="workDir"
          label="工作路径"
          tooltip={{
            title: '输入容器的工作目录',
            icon: <InfoCircleOutlined />,
          }}
          rules={[{ required: false }]}
        >
          <Input placeholder="输入容器的工作目录" />
        </Form.Item>
        <Form.Item
          name="source"
          label="资源规格"
          rules={[{ required: true, message: '请选择资源规格' }]}
        >
          <Select
            placeholder="请选择资源规格"
            showSearch
            filterOption={(input, option) =>
              (option?.children ?? '').includes(input)
            }
          >
            {sourceDatasource.map(({ id, name }) => (
              <Option key={id} value={name}>
                <Tooltip title={name}>{name}</Tooltip>
              </Option>
            ))}
          </Select>
        </Form.Item>
      </Form>
    </div>
  );
};
JobsUpdate.context = ({ onCancel, onSubmit }) => (
  <Space>
    <Button onClick={onCancel}>取消</Button>
    <Button type="primary" onClick={onSubmit}>
      保存
    </Button>
  </Space>
);

JobsUpdate.path = ['/jobs/list/update', '/jobs/list/create', '/jobs/list/copy'];

export default JobsUpdate;
