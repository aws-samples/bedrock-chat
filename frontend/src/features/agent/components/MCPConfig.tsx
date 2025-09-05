import React, { useCallback, useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { MCPConfig as MCPConfigType, MCPServer, MCPServer as MCPServerType } from '../types';
import Button from '../../../components/Button';
import InputText from '../../../components/InputText';
import Toggle from '../../../components/Toggle';
import useBot from '../../../hooks/useBot';
import { PiPlus, PiTrash } from 'react-icons/pi';
import ButtonIcon from '../../../components/ButtonIcon';

type Props = {
    botId: string;
    mcpConfig: MCPConfigType;
    onChange: (mcpConfig: MCPConfigType) => void;
    isLoading: boolean;
    setIsLoading: (loading: boolean) => void;
};

export const MCPConfig = ({ botId, mcpConfig, onChange, isLoading, setIsLoading }: Props) => {
    const { t } = useTranslation();
    const [error, setError] = useState<string | null>(null);
    const [servers, setServers] = useState<MCPServerType[]>([]);
    const { testMcpServerConnection } = useBot();

    // Initialize servers from config
    useEffect(() => {
        try {
        // Handle both string and object config formats
        let parsedConfig: any;
        
        if (typeof mcpConfig === 'string') {
            try {
                parsedConfig = JSON.parse(mcpConfig);
            } catch (e) {
                // If not valid JSON, initialize with empty array
                setServers([]);
                return;
            }
        } else {
            parsedConfig = mcpConfig;
        }
        
        if (parsedConfig && typeof parsedConfig === 'object' && parsedConfig.apiEndpoint) {
            setServers([{
                name: parsedConfig.name || '',
                endpoint: parsedConfig.apiEndpoint || '',
                apiKey: parsedConfig.apiKey || null,
                secretArn: parsedConfig.secretArn || null,
                tools: parsedConfig.tools || []
            }]);
        } 
        else if (Array.isArray(parsedConfig)) {
                setServers(parsedConfig.map(server => ({
                    name: server.name || '',
                    endpoint: server.apiEndpoint || '',
                    apiKey: server.apiKey || null,
                    secretArn: server.secretArn || null,
                    tools: server.tools || []
            })));
        }
        else {
            setServers([]);
        }
        } catch (e) {
            console.error('Error parsing config:', e);
            setServers([]);
        }
    }, []);


    // Update parent component when servers change
    useEffect(() => {
        const mcpConfig: MCPConfigType = {
            toolType: "mcp",
            name: "MCP Tool Configutaion",
            description: "MCP Server Configuration",
            mcpServers: servers
        };
        onChange(mcpConfig);
    }, [servers, onChange]);

    // Add a new server
    const addServer = useCallback(() => {
        setServers([
        ...servers,
        {
            name: "",
            endpoint: "",
            apiKey: "",
            secretArn: "",
            tools: {
                available: [],
                selected: []
            }
        }
        ]);
    }, [servers]);

    // Remove a server
    const removeServer = useCallback((indexToRemove: number) => {
          setServers(prevServers => prevServers.filter((_, index) => index !== indexToRemove));
    }, []);
    
    // Update a server
    const updateServer = useCallback((index: number, field: keyof MCPServerType, value: any) => {
        setServers(prevServers => {
            const updated = [...prevServers];
            updated[index] = {
                ...updated[index],
                [field]: value
            };
            return updated;
        });
    }, [servers]);

    // Toggle tool selection
    const toggleToolSelection = useCallback((serverIndex: number, toolName: string) => {
        setServers(prevServers => prevServers.map((server, sIndex) => {
            if (sIndex !== serverIndex) return server;

            const updatedTools = server.tools.selected.includes(toolName)
                ? server.tools.selected.filter(tool => tool !== toolName)
                : [...server.tools.selected, toolName];

            return {
                ...server,
                tools: {
                    ...server.tools,
                    selected: updatedTools
                }
            };
        }));
    }, []);

    const fetchTools = useCallback((server: MCPServer, index: number) => {
        setIsLoading(true);
        setError(null);
        
        // Validate server config
          if (!server.name) {
            setError('MCP Server Name is required');
            setIsLoading(false);
            return;
        }

        if (!server.endpoint) {
            setError('API endpoint is required');
            setIsLoading(false);
            return;
        }
        
        testMcpServerConnection(botId, server)
            .then(response => {
                // Update the server with the available tools returned from the backend
                updateServer(index, 'tools', {
                    available: response.data.tools.available || [],
                    selected: servers[index].tools?.selected || []
                });
                setIsLoading(false);
            })
            .catch(err => {
                setError(`Connection failed: ${err.message || 'Unknown error'}`);
                setIsLoading(false);
            });


    }, [setIsLoading, updateServer]);


    return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-medium">{t('agent.tools.mcp.config.title')}</h3>
        <ButtonIcon
          onClick={addServer}
          disabled={isLoading}
          >
          <PiPlus></PiPlus>
          {t('agent.tools.mcp.config.addServer')}
        </ButtonIcon>
      </div>
      
      {error && (
        <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-md">
          {error}
        </div>
      )}
      
      {servers.length === 0 ? (
        <div className="text-center p-6 border border-dashed border-gray-300 rounded-md">
          <p className="text-gray-500">{t('agent.tools.mcp.config.noServers')}</p>
          <ButtonIcon
            onClick={addServer}
            disabled={isLoading}
            className="mt-3 mr-auto ml-auto">
            <PiPlus></PiPlus>
            {t('agent.tools.mcp.config.addFirstServer')}
          </ButtonIcon>
        </div>
      ) : (
        servers.map((server, index) => (
          <div key={index} className="p-4 border border-gray-200 rounded-md space-y-4">
            <div className="flex justify-between items-center">
              <h4 className="font-medium">
                {t('agent.tools.mcp.config.server')} {index + 1}
              </h4>
              <ButtonIcon
                onClick={() => removeServer(index)}
                disabled={isLoading}
                >
                <PiTrash></PiTrash>
                {t('agent.tools.mcp.config.remove')}
              </ButtonIcon>
            </div>
            
            <div className="grid grid-cols-1 gap-4">
            <InputText
            label={t('agent.tools.mcp.config.name')}
            placeholder={t('agent.tools.mcp.config.namePlaceholder')}
            value={server.name}
            onChange={(e) => updateServer(index, 'name', e)}
            disabled={isLoading}
            />

            <InputText
            label={t('agent.tools.mcp.config.endpoint')}
            placeholder={t('agent.tools.mcp.config.endpointPlaceholder')}
            value={server.endpoint}
            onChange={(e) => updateServer(index, 'endpoint', e)}
            disabled={isLoading}
            />
              
            <InputText
            label={t('agent.tools.mcp.config.apiKey')}
            placeholder={t('agent.tools.mcp.config.apiKeyPlaceholder')}
            type="password"
            value={server.apiKey || ""}
            onChange={(e) => updateServer(index, 'apiKey', e)}
            disabled={isLoading}
            />
        
            <Button
            onClick={() => fetchTools(server, index)}
            loading={isLoading}
            disabled={isLoading || !server.name || !server.endpoint}>
            {t('agent.tools.mcp.config.connect')}
            </Button>

            {/* Available Tools Section */}
            {server.tools && server.tools.available.length > 0 && (
                <div className="mt-4">
                    <h5 className="font-medium mb-2">{t('agent.tools.mcp.config.tools')}</h5>
                    <div className="border border-gray-200 rounded-md divide-y">
                        {server.tools.available.map((toolItem, toolIndex) => (
                            <div 
                                key={toolItem.name} 
                                className="p-3 flex items-start hover:bg-gray-50"
                            >
                                <Toggle
                                    label={toolItem.name}
                                    value={server.tools.selected.includes(toolItem.name)}
                                    onChange={() => toggleToolSelection(index, toolItem.name)}
                                    className="mt-1 mr-3"
                                />
                                <div>
                                    <div className="font-medium">
                                        {toolItem.name}
                                    </div>
                                    <div className="text-sm text-gray-500">
                                        {toolItem.description}
                                    </div>
                                    {toolItem.inputSchema && toolItem.inputSchema.length > 0 && (
                                        <div className="text-xs text-gray-400 mt-1">
                                            Required: {toolItem.inputSchema.join(', ')}
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
                )}
                            
                {/* No tools message */}
                {(!server.tools || server.tools.available.length === 0) && (
                    <div className="text-center p-4 border border-dashed border-gray-200 rounded-md">
                        <p className="text-gray-500">
                            {t('agent.tools.mcp.config.noToolsAvailable')}
                        </p>
                    </div>
                )}
            </div>
            </div>
                ))
            )}
        </div>
    );
};
