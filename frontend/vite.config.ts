import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
    host: '0.0.0.0', // 监听所有地址，使开发服务器可被外部访问
    port: 5173,      // 可选，指定端口
  },
  preview: {
    host: '0.0.0.0', // 使预览服务器也可被外部访问
    port: 4173       // 预览服务器默认端口为4173，可根据需要修改
  }
})
