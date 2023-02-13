/*
 * @Author: junshi clayton.wang@digitalbrain.cn
 * @Date: 2023-02-10 15:37:21
 * @LastEditors: junshi clayton.wang@digitalbrain.cn
 * @LastEditTime: 2023-02-10 18:24:20
 * @FilePath: /huanghe/source/services/frontend/src/common/components/LogMonitor/index.js
 * @Description:
 */
import InfiniteScroll from 'react-infinite-scroll-component';
import { List, Skeleton, Divider } from 'antd';
import { useEffect, useState } from 'react';
import './index.less';
const LogMonitor = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState([]);

  const loadMoreData = () => {
    if (loading) {
      return;
    }
    setLoading(true);
    fetch(
      'https://randomuser.me/api/?results=10&inc=name,gender,email,nat,picture&noinfo'
    )
      .then((res) => res.json())
      .then((body) => {
        setData([...data, ...body.results]);
        setLoading(false);
      })
      .catch(() => {
        setLoading(false);
      });
  };

  useEffect(() => {
    loadMoreData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="detail-log-list">
      <div className="content" id="scrollableDiv">
        <InfiniteScroll
          dataLength={data.length}
          next={loadMoreData}
          hasMore={data.length < 50}
          loader={
            <Skeleton
              paragraph={{
                rows: 1,
              }}
              active
            />
          }
          endMessage={<Divider plain>日志结束</Divider>}
          scrollableTarget="scrollableDiv"
        >
          <List
            bordered={false}
            size="small"
            split={false}
            dataSource={data}
            renderItem={(item) => (
              <List.Item key={item.email}>
                <div>Content</div>
              </List.Item>
            )}
          />
        </InfiniteScroll>
      </div>
    </div>
  );
};

export default LogMonitor;
