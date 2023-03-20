/**
 * @Author guanlin.li guanlin.li@digitalbrain.cn
 * @Date 2022-12-22 10:48:26
 * @LastEditors guanlin.li guanlin.li@digitalbrain.cn
 * @LastEditTime 2022-12-23 09:40:59
 * @Description Service新建/编辑页
 */
import { useEffect, useState, useMemo, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Button,
  Form,
  Input,
  message,
  Select,
  Tooltip,
  Space,
  Switch,
} from 'antd';
import { get } from 'lodash';
import { InfoCircleOutlined } from '@ant-design/icons';
import api from '@/common/api';
import { CREATE, UPDATE, ADMIN } from '@/common/constants';
import { useContextProps } from '@/common/hooks/RoutesProvider';
import { useAuth } from '@/common/hooks/useAuth';
import { ID } from '@/common/utils/helper';
import './index.less';

const { Option } = Select;

const ServicesUpdate = () => {
  const [projectsDatasource, setProjectsDatasource] = useState([]);
  const [imagesDatasource, setImagesDatasource] = useState([]);
  const [sourceDatasource, setSourceDatasource] = useState([]);
  const setContextProps = useContextProps();
  const [type, setType] = useState(CREATE);
  const serviceUniqueID = useRef();
  const { user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [form] = Form.useForm();

  const requestService = async (params) => {
    try {
      const { result } = await api.servicesDetail({ ...params });
      form.setFieldsValue(result);
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
      const { result } = await api.imagesList();
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
      const { result } = await api.sourceList();
      setSourceDatasource(result.data);
    } catch (error) {
      console.log(error);
    }
  };
  // const requestStorages = async () => {
  //   try {
  //     const { result } = await api.storagesList({
  //       filter: { isdeleted: false },
  //     });
  //     setStoragesDatasource(
  //       result.data.map(({ id, ...rest }) => ({ id: Number(id), ...rest }))
  //     );
  //   } catch (error) {
  //     console.log(error);
  //   }
  // };
  const saveService = async (values) => {
    try {
      await api.servicesListCreate(values);
      message.success('创建成功！');
      backToList();
    } catch (error) {
      console.log(error);
    }
  };
  const updateService = async (values) => {
    try {
      await api.servicesListUpdate(values);
      message.success('保存成功!');
      backToList();
    } catch (error) {
      console.log(error);
    }
  };

  const backToList = () => {
    navigate('/services/list', { state: null });
  };
  const handleSubmit = () => {
    const values = form.getFieldsValue();
    const { id = null } = get(location, 'state.params', {});
    console.log(values);
    if (type === CREATE) {
      saveService(values);
    } else {
      updateService({ id, ...values });
    }
  };
  const handleSubmitFailed = ({ errorFields }) => {
    message.error(errorFields[0].errors[0]);
    console.log(errorFields);
  };
  const handleCancelClicked = () => {
    backToList();
  };

  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    requestProjects();
    requestImages();
    requestSource();
    serviceUniqueID.current = new ID();
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
    if (type === UPDATE) {
      requestService({ id });
    } else {
      form.setFieldsValue({
        project: projectDefaultValue,
        image: imageDefaultValue,
        isPublic: 'checked',
      });
    }
    setType(type);
  }, [location, form, projectDefaultValue, imageDefaultValue]);

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
  return (
    <div className="services-update">
      <Form
        className="services-update-form"
        form={form}
        layout="vertical"
        onFinish={handleSubmit}
        onFinishFailed={handleSubmitFailed}
        onCancel={handleCancelClicked}
      >
        <Form.Item
          name="name"
          label="名称"
          rules={[
            { required: true, message: '请输入Service名称' },
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
          <Input placeholder="请输入Service名称" disabled={type === UPDATE} />
        </Form.Item>
        <Form.Item
          name="project"
          label="项目"
          rules={[{ required: true, message: '请选择项目' }]}
        >
          <ProjectSelect />
        </Form.Item>
        <Form.Item
          name="image"
          label="镜像"
          rules={[{ required: true, message: '请选择镜像' }]}
        >
          <Input placeholder="输入镜像地址" />
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
        <Form.Item name="isPublic" label="公网访问" valuePropName="checked">
          <Switch checkedChildren="是" unCheckedChildren="否" />
        </Form.Item>
        {/* <MyFormItem name="isPublic" label="公网访问" valuePropName="checked">
          <Switch />
          {(form.getFieldValue('isPublic') === 'checked' && ' 是') || ' 否'}
        </MyFormItem> */}
      </Form>
    </div>
  );
};
ServicesUpdate.context = ({ onCancel, onSubmit }) => (
  <Space>
    <Button onClick={onCancel}>取消</Button>
    <Button type="primary" onClick={onSubmit}>
      保存
    </Button>
  </Space>
);

ServicesUpdate.path = ['/services/list/update/:id', '/services/list/create'];

export default ServicesUpdate;
