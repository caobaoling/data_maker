import request from './request'

// 生成词云
export function generateWordCloud(data) {
  return request({
    url: '/api/tools/wordcloud',
    method: 'post',
    data
  })
}

// 获取 hosts 文件列表
export function getHostsFiles() {
  return request({
    url: '/api/tools/hosts_files',
    method: 'get'
  })
}
