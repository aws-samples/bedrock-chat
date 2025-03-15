import { useEffect, useState } from 'react';
import useGroupApi from './useGroupApi';
import { Group } from '../@types/group';

const useGroup = () => {

    const api = useGroupApi();
    const [myGroups, setMyGroups] = useState<Record<string, Group>>();
    const [isAdmin, setIsAdmin] = useState(false);
    const [isAssistantCreator, setIsAssistantCreator] = useState(false);

    useEffect(() => {
        const fetchGroups = async () => {
            try {
                const response = await api.getGroupListApi();

                const groupMap: Record<string, Group> = {};
                for (const group of response.data) {
                    groupMap[group.groupId] = group;
                }
                setMyGroups(groupMap);
                if (response.data && Array.isArray(response.data) && response.data.length > 0) {
                    setIsAssistantCreator(true);
                }
                if (response.data?.some(group => group.role.toUpperCase().includes("ADMIN"))) {
                    setIsAdmin(true);
                }
            } catch (error) {
                console.error('Error fetching groups:', error);
            }
        };

        fetchGroups();
    }, []);

    return {
        myGroups,
        isAdmin,
        isAssistantCreator,
        getGroupList: async () => {
            return (await api.getGroupListApi()).data;
        },
    }
}

export default useGroup;