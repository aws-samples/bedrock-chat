import useGroupApi from './useGroupApi';

const useGroup = () => {

    const api = useGroupApi();

    return {
        getGroupList: async () => {
            return (await api.getGroupListApi()).data;
          },
    }
}

export default useGroup;