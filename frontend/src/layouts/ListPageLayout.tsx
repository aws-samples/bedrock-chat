import React, { ReactNode } from 'react';
import Help from '../components/Help';
import { TooltipDirection } from '../constants';
import Skeleton from '../components/Skeleton';

type Props = {
  pageTitle: string;
  pageTitleHelp?: string;
  pageTitleActions?: ReactNode;
  searchCondition?: ReactNode;
  isLoading?: boolean;
  isEmpty?: boolean;
  emptyMessage?: string;
  children: ReactNode;
};

const ListPageLayout: React.FC<Props> = (props) => {
  return (
    <div className="flex h-full justify-center">
      <div className="w-full max-w-screen-xl px-4 lg:w-4/5">
        <div className="size-full pt-8">
          <div className="flex justify-between">
            <div className="flex items-center gap-2">
              <h1 className="font-heading text-xl font-bold tracking-tight">{props.pageTitle}</h1>
              {props.pageTitleHelp && (
                <Help
                  direction={TooltipDirection.RIGHT}
                  message={props.pageTitleHelp}
                />
              )}
            </div>
            {props.pageTitleActions && <div>{props.pageTitleActions}</div>}
          </div>
          {props.searchCondition && (
            <div className="my-3">{props.searchCondition}</div>
          )}
          <div className="mt-3 border-b border-black/[0.06] dark:border-white/[0.06]"></div>

          <div className="-mr-2 h-[calc(100%-3rem)] overflow-x-auto overflow-y-scroll scrollbar-thin scrollbar-thumb-aws-font-color-light/20 dark:scrollbar-thumb-aws-font-color-dark/20">
            <div className="mr-2 h-full pb-8">
              {props.isLoading && (
                <div className="mt-4 flex flex-col gap-3">
                  {new Array(8).fill('').map((_, idx) => (
                    <Skeleton key={idx} className="h-14 w-full rounded-xl" />
                  ))}
                </div>
              )}
              {!props.isLoading && props.isEmpty && (
                <div className="flex size-full items-center justify-center text-sm text-dark-gray dark:text-light-gray">
                  {props.emptyMessage}
                </div>
              )}
              {!props.isLoading && !props.isEmpty && (
                <div className="mt-3 flex flex-col gap-2">
                  {props.children}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ListPageLayout;
