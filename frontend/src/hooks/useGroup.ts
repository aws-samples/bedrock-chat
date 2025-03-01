import { useEffect, useState } from 'react';
import useGroupApi from './useGroupApi';
import { GetGroupListResponse } from '../@types/group';

const useGroup = () => {

    const api = useGroupApi();
    const [myGroups, setMyGroups] = useState<GetGroupListResponse>();

    useEffect(() => {
        const fetchGroups = async () => {
            try {
                const response = await api.getGroupListApi();
                setMyGroups(response.data);
            } catch (error) {
                console.error('Error fetching groups:', error);
            }
        };

        fetchGroups();
    }, []);

    return {
        myGroups,
        getGroupList: async () => {
            return (await api.getGroupListApi()).data;
        },
    }
}

export default useGroup;