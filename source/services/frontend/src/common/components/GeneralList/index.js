/**
 * @description 通用数据列表
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { useEffect, useState, useCallback } from 'react';
import { Form, message, Upload } from 'antd';
import { find } from 'lodash';
import { DownloadOutlined } from '@ant-design/icons';
import { transformDate } from '@/common/utils/helper';
import AuthButton from '@/common/components/AuthButton';
import GeneralTable from '@/common/components/GeneralList/table';

const GeneralList = ({ fetch, upload, download, update, required }) => {
  const [columns, setColumns] = useState([]);
  const [dataSource, setDataSource] = useState([]);
  const [loading, setLoading] = useState(false);
  const [updatedRows, setUpdateRows] = useState(new Set());
  const [form] = Form.useForm();
  const requestList = useCallback(async () => {
    try {
      setLoading(true);
      const data = await fetch();
      const { columns: _cols, data: _data } = data.result;
      setColumns(_cols);
      setDataSource(_data);
      setLoading(false);
    } catch (error) {
      console.log(error);
      setLoading(false);
    }
  }, [fetch]);

  useEffect(() => {
    requestList();
  }, [requestList]);

  const reload = () => {
    requestList();
  };
  const formatBeforeSave = (data) =>
    data.map((item) => {
      const result = { ...item };
      Object.keys(item).forEach((key) => {
        const col = find(columns, ['dataIndex', key]);
        if (col) {
          const dataType = col.dataType;
          if (dataType === 'DATE') {
            result[key] = transformDate(item[key]);
          }
        }
      });
      return result;
    });
  const handleSaveClicked = async () => {
    try {
      const updatedData = [...updatedRows].map((id) =>
        find(dataSource, ['id', id])
      );
      const result = formatBeforeSave(updatedData);
      await update({ data: JSON.stringify(result) });
      message.success('数据保存成功！');
      console.log(updatedData);
    } catch (_err) {
      message.error('数据保存失败！');
    }
  };
  const handleUploadChange = ({ file }) => {
    const { response, status } = file;
    const uploadFailed = () => {
      const msg = (response && response.message) || '文件上传失败！';
      message.error(msg);
    };
    const uploadSuccess = () => {
      const msg =
        (response && response.message) ||
        (file.name && `${file.name}上传成功！`) ||
        '文件上传成功！';
      message.success(msg);
    };
    if (status === 'done') {
      uploadSuccess();
      reload();
    } else if (status === 'error') {
      uploadFailed();
    }
  };
  const handleDownloadClicked = () => {
    download();
  };
  const handleTableUpdate = (record) => {
    const newData = [...dataSource];
    const index = newData.findIndex((item) => record.id === item.id);
    if (index > -1) {
      const item = newData[index];
      newData.splice(index, 1, {
        ...item,
        ...record,
      });
      setDataSource(newData);
    } else {
      newData.push(record);
      setDataSource(newData);
    }
    setUpdateRows(updatedRows.add(record.id));
  };

  return (
    <div className="dbr-table-container">
      <Form form={form} component={false}>
        <div className="batch-command">
          <AuthButton
            required={required}
            style={{ float: 'left' }}
            type="primary"
            className="batch-command-item"
            onClick={handleSaveClicked}
            htmlType="submit"
          >
            保存
          </AuthButton>
          <Upload
            {...upload}
            multiple={false}
            accept=".xlsx,.xls"
            showUploadList={false}
            onChange={handleUploadChange}
            className="upload-btn batch-command-item"
          >
            <AuthButton required={required}>上传</AuthButton>
          </Upload>
          <span className="dbr-table-description">
            编辑数据后请点击保存按钮，上传后的数据会覆盖原有数据
          </span>
          <AuthButton
            required={required}
            style={{ float: 'right' }}
            onClick={handleDownloadClicked}
            type="link"
            className="batch-command-item"
            icon={<DownloadOutlined />}
          >
            模板
          </AuthButton>
        </div>
        <GeneralTable
          loading={loading}
          columns={columns}
          dataSource={dataSource}
          onUpdate={handleTableUpdate}
          required={required}
        />
      </Form>
    </div>
  );
};
export default GeneralList;
