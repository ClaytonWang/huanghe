/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-01-31 16:10:19
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-01-31 17:29:19
 * @FilePath: /frontend/src/pages/jobs/update/index.js
 * @Description: Job新建 / 编辑页;
 */
import { useEffect, useState, useMemo, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Button, Divider, Form, Input, message, Select, Tooltip } from 'antd';
import { uniqueId, get, map, drop } from 'lodash';
import {
  DeleteFilled,
  InfoCircleOutlined,
  PlusOutlined,
} from '@ant-design/icons';
import api from '@/common/api';
import { CREATE, UPDATE, ADMIN } from '@/common/constants';
import { useAuth } from '@/common/hooks/useAuth';
import { genUniqueIdByPrefix, ID } from '@/common/utils/helper';
import './index.less';

const { Option } = Select;

const JobsUpdate = () => {
  const [projectsDatasource, setProjectsDatasource] = useState([]);
  const [imagesDatasource, setImagesDatasource] = useState([]);
  const [sourceDatasource, setSourceDatasource] = useState([]);
  const [storagesDatasource, setStoragesDatasource] = useState([]);
  const [selectedStorages, setSelectedStorages] = useState([]);
  const [type, setType] = useState(CREATE);
  const notebookUniqueID = useRef();
  const { user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [form] = Form.useForm();

  const updateSelectedStorage = (values, transform) => {
    let result = [];
    if (transform) {
      result = transform(values);
    } else {
      result = map(get(values, 'hooks', []), 'storage');
    }
    setSelectedStorages([...result]);
  };

  const requestNotebook = async (params) => {
    try {
      const { result } = await api.notebooksDetail({ ...params });
      form.setFieldsValue(result);
      updateSelectedStorage(result);
    } catch (error) {
      console.log(error);
    }
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
  const requestImages = async () => {
    try {
      const { result } = await api.imagesList();
      setImagesDatasource(result.data);
    } catch (error) {
      console.log(error);
    }
  };
  const requestSource = async () => {
    try {
      const { result } = await api.sourceList();
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
  const saveNotebook = async (values) => {
    try {
      await api.notebooksListCreate(values);
      message.success('创建成功！');
      backToList();
    } catch (error) {
      console.log(error);
    }
  };
  const updateNotebook = async (values) => {
    try {
      await api.notebooksListUpdate(values);
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
        values.map(({ storage }) => storage || false).filter((value) => value)
      );
    }
  };
  const handleSubmit = () => {
    const values = form.getFieldsValue();
    const { id = null } = get(location, 'state.params', {});
    if (type === CREATE) {
      saveNotebook(values);
    } else {
      updateNotebook({ id, ...values });
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

  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    requestProjects();
    requestImages();
    requestSource();
    requestStorages();
    notebookUniqueID.current = new ID();
  }, []);

  useEffect(() => {
    const { id = null } = get(location, 'state.params', {});
    const type = get(location, 'state.type');
    if (type === UPDATE) {
      requestNotebook({ id });
    } else {
      form.setFieldsValue({
        hooks: [
          {
            path: '/home/jovyan',
          },
        ],
      });
    }
    setType(type);
  }, [location]);

  const HooksItem = ({ name, remove, selectedStorages, disabledItems }) => {
    const currStorage = form.getFieldValue(['hooks', name, 'storage']);
    const filteredStorageOptions = useMemo(() => {
      const result = storagesDatasource.filter(
        ({ id }) => !(selectedStorages.includes(id) && id !== currStorage)
      );
      return result;
    }, [selectedStorages, storagesDatasource]);
    return (
      <>
        <div className="notebooks-hooks-item">
          <span className="content">
            <Form.Item
              name={[name, 'storage']}
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
            { required: true, message: '请输入Notebook名称' },
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
          <Input placeholder="请输入Notebook名称" />
        </Form.Item>
        <Form.Item
          name="image"
          label="镜像"
          rules={[{ required: true, message: '请选择镜像' }]}
        >
          <Select
            placeholder="请选择镜像"
            showSearch
            filterOption={(input, option) =>
              (option?.children ?? '').includes(input)
            }
          >
            {imagesDatasource.map(({ id, name }) => (
              <Option key={id} value={id}>
                <Tooltip title={name}>{name}</Tooltip>
              </Option>
            ))}
          </Select>
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
              <Option key={id} value={id}>
                <Tooltip title={name}>{name}</Tooltip>
              </Option>
            ))}
          </Select>
        </Form.Item>
        <Form.Item
          name="project"
          label="所属项目"
          rules={[{ required: true, message: '请选择项目' }]}
        >
          <Select placeholder="请选择项目">
            {projectsDatasource.map(({ id, name = '-' }) => (
              <Option key={id} value={id}>
                {name}
              </Option>
            ))}
          </Select>
        </Form.Item>
        <Form.List
          name="hooks"
          rules={[
            {
              validator: async (_, hooks) => {
                if (!hooks || hooks.length < 1) {
                  return Promise.reject(new Error('至少一个挂载'));
                }
              },
            },
          ]}
        >
          {(fields = [], { add, remove }, { errors }) => (
            <>
              <Form.Item label="存储挂载" wrapperCol={{ push: 2, xs: 22 }}>
                {
                  <HooksItem
                    key={uniqueId('hook-')}
                    {...fields[0]}
                    selectedStorages={selectedStorages}
                    disabledItems={['path']}
                  />
                }
                {drop([...fields], 1).map((field) => (
                  <HooksItem
                    key={uniqueId('hook-')}
                    {...field}
                    remove={remove}
                    selectedStorages={selectedStorages}
                  />
                ))}
                <Button
                  style={{ width: '100%' }}
                  onClick={() =>
                    add({
                      path: `/home/jovyan/${genUniqueIdByPrefix(
                        'vol-',
                        notebookUniqueID.current
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
        <Form.Item>
          <Button onClick={handleCancelClicked}>取消</Button>
          <Button type="primary" htmlType="submit">
            保存
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};
export default JobsUpdate;
