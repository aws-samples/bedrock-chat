export type Group = {
    groupId: string;
    groupName: string;
    createTime: Date;
    updateTime: Date;
    createBy: string;
    role: string;
    ltiName: string;
}

export type GetGroupListResponse = Group[];


export type AssistantGroupType = {
    label: string;
    value: string;
  }