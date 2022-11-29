/**
 * @description 通用表格
 * @author liguanlin<guanlin.li@digitalbrain.cn>
 */
import { DatePicker, Form, InputNumber, Table, Input } from 'antd';
import { useCallback, useState } from 'react';

import moment from 'moment';
import { formatNumber, transformDate } from '@/common/utils/helper';
import AuthButton from '../AuthButton';

const GeneralTable = ({
  columns = [],
  loading = false,
  dataSource = [],
  onUpdate = () => {},
  required = '',
}) => {
  const form = Form.useFormInstance();
  const [editingKey, setEditingKey] = useState(null);

  const isEditing = useCallback(
    (record) => record.id === editingKey,
    [editingKey]
  );
  const edit = useCallback(
    (record) => {
      console.log('edit', record);
      form.setFieldsValue({ ...record });
      setEditingKey(record.id);
    },
    [form]
  );

  const cancel = () => {
    setEditingKey(null);
  };

  const save = useCallback(
    async (key) => {
      try {
        const row = await form.validateFields();
        onUpdate({ id: key, ...row });
        setEditingKey(null);
      } catch (errInfo) {
        console.log('Validate Failed:', errInfo);
      }
    },
    [form, onUpdate]
  );

  const EditableCell = ({
    editing,
    dataIndex,
    inputType,
    children,
    ...restProps
  }) => {
    let inputNode = <Input />;
    if (inputType === 'number') {
      inputNode = <InputNumber />;
    } else if (inputType === 'date') {
      inputNode = <DatePicker format="YYYY/MM/DD" />;
    }

    return (
      <td {...restProps}>
        {editing ? (
          <Form.Item name={dataIndex} style={{ margin: 0 }}>
            {inputNode}
          </Form.Item>
        ) : (
          children
        )}
      </td>
    );
  };
  const genColumns = useCallback(() => {
    const cols = columns.map(({ title, dataIndex, dataType }) => ({
      title,
      dataIndex,
      render: (value) => {
        if (!value) {
          return '-';
        }
        if (dataType === 'DOUBLE') {
          return formatNumber(value);
        }
        if (dataType === 'DATE') {
          return transformDate(value);
        }
        return value;
      },
      editable: true,
      onCell: (record) => {
        let inputType = 'text';
        if (['DOUBLE', 'INT'].indexOf(dataType) > -1) {
          inputType = 'number';
        } else if (['DATE'].indexOf(dataType) > -1) {
          inputType = 'date';
          const date = record[dataIndex];
          record[dataIndex] = date ? moment(date) : date;
        }
        return {
          record,
          inputType,
          dataIndex,
          title,
          editing: isEditing(record),
        };
      },
    }));
    cols.push({
      title: '操作',
      dataIndex: 'operation',
      fixed: 'right',
      width: 150,
      render: (_, record) => {
        const editable = isEditing(record);
        return editable ? (
          <span>
            <AuthButton
              required={required}
              onClick={() => save(record.id)}
              type="link"
              style={{ marginRight: 8 }}
            >
              确认
            </AuthButton>
            <AuthButton
              required={required}
              onClick={() => cancel()}
              type="link"
            >
              取消
            </AuthButton>
          </span>
        ) : (
          <AuthButton
            required={required}
            disabled={editingKey !== null}
            onClick={() => edit(record)}
            type="link"
          >
            编辑
          </AuthButton>
        );
      },
    });
    return cols;
  }, [columns, editingKey, edit, isEditing, required, save]);

  const pagination = {
    total: dataSource.length,
    pagesize: 10,
    showSizeChanger: false,
  };

  return (
    <Table
      size="small"
      rowKey="id"
      scroll={{ x: 'max-content' }}
      components={{
        body: {
          cell: EditableCell,
        },
      }}
      loading={loading}
      columns={genColumns()}
      dataSource={dataSource}
      pagination={pagination}
    />
  );
};
export default GeneralTable;
