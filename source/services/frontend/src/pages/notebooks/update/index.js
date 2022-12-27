/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-12-22 10:48:26
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-23 09:40:59
 * @Description Notebook新建/编辑页
 */
import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Button, Divider, Form, Input, message, Select } from 'antd';
import { uniqueId, get } from 'lodash';
import { DeleteFilled, PlusOutlined } from '@ant-design/icons';
import api from '@/common/api';
import { CREATE, UPDATE } from '@/common/constants';
import './index.less';

const { Option } = Select;

const NotebooksUpdate = () => {
  const [projectsDatasource, setProjectsDatasource] = useState([]);
  const [imagesDatasource, setImagesDatasource] = useState([]);
  const [sourceDatasource, setSourceDatasource] = useState([]);
  const [storagesDatasource, setStoragesDatasource] = useState([]);
  const [type, setType] = useState(CREATE);
  const navigate = useNavigate();
  const location = useLocation();
  const [form] = Form.useForm();

  const requestNotebook = async (params) => {
    try {
      const { result } = await api.notebooksDetail({ ...params });
      form.setFieldsValue(result);
    } catch (error) {
      console.log(error);
    }
  };

  const requestProjects = async () => {
    try {
      const { result } = await api.bamProjectsList();
      setProjectsDatasource(result.data);
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
      const { result } = await api.storagesList();
      setStoragesDatasource(result.data);
    } catch (error) {
      console.log(error);
    }
  };
  const saveNotebook = async (values) => {
    try {
      await api.notebooksListCreate(values);
      const msg = (type === CREATE && '创建成功！') || '保存成功';
      message.success(msg);
      backToList();
    } catch (error) {
      console.log(error);
    }
  };
  const backToList = () => {
    navigate('/notebooks/list', { state: null });
  };
  const handleSubmit = () => {
    const values = form.getFieldsValue();
    const { id = null } = get(location, 'state.params', {});
    if (id) {
      saveNotebook({ id, ...values });
    } else {
      saveNotebook(values);
    }
    console.log('values,', values);
  };
  const handleCancelClicked = () => {
    backToList();
  };

  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    requestProjects();
    requestImages();
    requestSource();
    requestStorages();
  }, []);

  useEffect(() => {
    const { id = null } = get(location, 'state.params', {});
    const type = get(location, 'state.type');
    if (type === UPDATE) {
      requestNotebook({ id });
    }
    setType(type);
  }, [location]);

  const HooksItem = ({ name, remove }) => (
    <>
      <div className="notebooks-hooks-item">
        <span className="content">
          <Form.Item
            name={[name, 'storage']}
            label="存储盘"
            rules={[{ required: true, message: '请选择存储盘' }]}
          >
            <Select
              placeholder="请选择资源规格"
              showSearch
              filterOption={(input, option) =>
                (option?.children ?? '').includes(input)
              }
            >
              {storagesDatasource.map(({ id, name, config }) => (
                <Option key={id} value={id}>
                  {`${name} ${config.value}/${config.size}`}
                </Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item
            name={[name, 'path']}
            label="目录"
            rules={[{ required: true, message: '请输入存储目录' }]}
          >
            <Input placeholder="请输入目录" />
          </Form.Item>
        </span>
        <span className="action">
          <DeleteFilled onClick={() => remove(name)} />
        </span>
      </div>
      <Divider />
    </>
  );

  return (
    <div className="notebooks-update">
      <Form
        className="notebooks-update-form"
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        onCancel={handleCancelClicked}
      >
        <Form.Item
          name="name"
          label="名称"
          rules={[{ required: true, message: '请输入Notebook名称' }]}
        >
          <Input placeholder="请输入Notebook名称" />
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
                {name}
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
          {(fields, { add, remove }, { errors }) => (
            <>
              <Form.Item label="存储挂载" wrapperCol={{ push: 2, xs: 22 }}>
                {fields.map((field) => (
                  <HooksItem
                    key={uniqueId('hook-')}
                    {...field}
                    remove={remove}
                  />
                ))}
                <Button
                  style={{ width: '100%' }}
                  onClick={() =>
                    add({ path: `/home/jovyan/${uniqueId('vol-')}` })
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
export default NotebooksUpdate;
