/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-02-01 18:03:06
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-16 17:53:53
 * @FilePath: /huanghe/source/services/frontend/src/common/components/Monitor/index.js
 * @Description: 监控公共组建
 */
import React from 'react';
import './index.less';

const ChartMonitor = ({ urls = {}, dateRange, style = { height: 200 } }) => {
  const time = `&theme=light&from=${dateRange?.from?.valueOf()}&to=${dateRange?.to?.valueOf()}`;
  return (
    <>
      {Object.keys(urls)?.map((key, index) => {
        const grafana = urls?.[key] ?? ``;
        if (!grafana) return null;
        return (
          <div key={index} className="detail-chart-list">
            <iframe
              name="iframe"
              className="content"
              style={style}
              src={grafana + time}
            />
          </div>
        );
      })}
    </>
  );
};

const areEqual = (preProps, nextProps) =>
  preProps.urls?.cpu === nextProps.urls?.cpu &&
  preProps.urls?.ram === nextProps.urls?.ram &&
  preProps.urls?.gpu === nextProps.urls?.gpu &&
  preProps.urls?.vram === nextProps.urls?.vram &&
  preProps.dateRange?.from?.valueOf() ===
    nextProps.dateRange?.from?.valueOf() &&
  preProps.dateRange?.to?.valueOf() === nextProps.dateRange?.to?.valueOf();

export default React.memo(ChartMonitor, areEqual);
