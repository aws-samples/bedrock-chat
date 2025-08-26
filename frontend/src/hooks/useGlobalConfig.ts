import useHttp from './useHttp';

interface GlobalConfig {
  globalAvailableModels?: string[] | null;
}

const useGlobalConfig = () => {
  const http = useHttp();

  return {
    getGlobalConfig: () => {
      return http.get<GlobalConfig>('config/global');
    },
  };
};

export default useGlobalConfig;
