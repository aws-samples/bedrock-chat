const translation = {
  translation: {
    signIn: {
      button: {
        login: 'Đăng nhập',
      },
    },
    app: {
      name: 'Bedrock Claude Chat',
      nameWithoutClaude: 'Bedrock Chat',
      inputMessage: 'Tôi có thể giúp gì cho bạn?',
      starredBots: 'Bot đã gắn sao',
      recentlyUsedBots: 'Bot đã sử dụng gần đây',
      conversationHistory: 'Lịch sử',
      chatWaitingSymbol: '▍',
      adminConsoles: 'Dành cho Quản trị viên',
    },
    model: {
      haiku3: {
        label: 'Claude 3 (Haiku)',
        description:
          'Phiên bản trước được tối ưu hóa về tốc độ và nhỏ gọn, cung cấp phản hồi gần như tức thì.',
      },
      sonnet3: {
        label: 'Claude 3 (Sonnet)',
        description: 'Cân bằng giữa tốc độ và trí thông minh.',
      },
      'sonnet3-5': {
        label: 'Claude 3.5 (Sonnet) v1',
        description:
          'Phiên bản Claude 3.5 ban đầu. Hỗ trợ nhiều nhiệm vụ, nhưng v2 cải thiện độ chính xác.',
      },
      'sonnet3-5-v2': {
        label: 'Claude 3.5 (Sonnet) v2',
        description:
          'Phiên bản mới nhất của Claude 3.5 với độ chính xác và hiệu suất cao hơn.',
      },
      'haiku3-5': {
        label: 'Claude 3.5 (Haiku)',
        description:
          'Phiên bản mới nhất với tốc độ phản hồi nhanh hơn và khả năng cải thiện so với Haiku 3.',
      },
      opus3: {
        label: 'Claude 3 (Opus)',
        description: 'Mô hình mạnh mẽ cho các tác vụ phức tạp.',
      },
      mistral7b: {
        label: 'Mistral 7B',
      },
      mistral8x7b: {
        label: 'Mixtral-8x7B',
      },
      mistralLarge: {
        label: 'Mistral Large',
      },
      novaPro: {
        label: 'Amazon Nova Pro',
        description:
          'Mô hình đa phương thức mạnh mẽ với độ chính xác, tốc độ và chi phí tối ưu.',
      },
      novaLite: {
        label: 'Amazon Nova Lite',
        description:
          'Mô hình chi phí thấp, tốc độ xử lý nhanh chóng cho hình ảnh, video và văn bản.',
      },
      novaMicro: {
        label: 'Amazon Nova Micro',
        description:
          'Mô hình văn bản với độ trễ thấp nhất và chi phí cực kỳ thấp.',
      },
    },
    agent: {
      label: 'Agent',
      help: {
        overview:
          'Chức năng Agent cho phép chatbot xử lý các nhiệm vụ phức tạp tự động.',
      },
      hint: `Agent tự động xác định công cụ cần sử dụng để trả lời câu hỏi của người dùng. Thời gian phản hồi sẽ dài hơn khi chức năng này được bật.`,
      progress: {
        label: 'Đang suy nghĩ...',
      },
      progressCard: {
        toolInput: 'Đầu vào: ',
        toolOutput: 'Đầu ra: ',
        status: {
          running: 'Đang chạy...',
          success: 'Thành công',
          error: 'Lỗi',
        },
      },
      tools: {
        get_weather: {
          name: 'Thời tiết hiện tại',
          description: 'Lấy dự báo thời tiết hiện tại.',
        },
        sql_db_query: {
          name: 'Truy vấn cơ sở dữ liệu',
          description: 'Thực hiện truy vấn SQL để lấy dữ liệu.',
        },
        sql_db_schema: {
          name: 'Lược đồ cơ sở dữ liệu',
          description: 'Lấy thông tin lược đồ và ví dụ bảng.',
        },
        sql_db_list_tables: {
          name: 'Liệt kê bảng dữ liệu',
          description: 'Liệt kê tất cả bảng trong cơ sở dữ liệu.',
        },
        sql_db_query_checker: {
          name: 'Kiểm tra truy vấn',
          description: 'Kiểm tra truy vấn SQL có hợp lệ hay không.',
        },
        internet_search: {
          name: 'Tìm kiếm trên Internet',
          description: 'Tìm kiếm thông tin trên Internet.',
        },
        knowledge_base_tool: {
          name: 'Lấy kiến thức',
          description: 'Lấy thông tin từ nguồn kiến thức.',
        },
      },
    },
    bot: {
      label: {
        myBots: 'Bot của tôi',
        recentlyUsedBots: 'Bot được chia sẻ sử dụng gần đây',
        knowledge: 'Kiến thức',
        url: 'URL',
        s3url: 'Nguồn dữ liệu S3',
        sitemap: 'URL sơ đồ trang web',
        file: 'Tập tin',
        loadingBot: 'Đang tải...',
        normalChat: 'Trò chuyện',
        notAvailableBot: '[KHÔNG khả dụng]',
        notAvailableBotInputMessage: 'Bot này KHÔNG khả dụng.',
        noDescription: 'Không có mô tả',
        notAvailable: 'Bot này KHÔNG khả dụng.',
        noBots: 'Không có Bot.',
        noBotsRecentlyUsed: 'Không có Bot được chia sẻ sử dụng gần đây.',
        retrievingKnowledge: '[Đang truy xuất kiến thức...]',
        selectParsingModel: 'Chọn mô hình phân tích',
        dndFileUpload:
          'Bạn có thể tải tệp lên bằng cách kéo và thả.\nTệp được hỗ trợ: {{fileExtensions}}',
        uploadError: 'Thông báo lỗi',
        referenceLink: 'Liên kết tham khảo',
        syncStatus: {
          queue: 'Đang chờ đồng bộ',
          running: 'Đang đồng bộ',
          success: 'Đồng bộ thành công',
          fail: 'Đồng bộ thất bại',
        },
        fileUploadStatus: {
          uploading: 'Đang tải lên...',
          uploaded: 'Đã tải lên',
          error: 'LỖI',
        },
        quickStarter: {
          title: 'Bắt đầu hội thoại nhanh',
          exampleTitle: 'Tiêu đề',
          example: 'Ví dụ hội thoại',
        },
        citeRetrievedContexts: 'Trích dẫn nội dung đã truy xuất',
        unsupported: 'Không được hỗ trợ, Chỉ đọc',
      },
      titleSubmenu: {
        edit: 'Chỉnh sửa',
        copyLink: 'Sao chép liên kết',
        copiedLink: 'Đã sao chép',
      },
    },
    deleteDialog: {
      title: 'Xóa?',
      content: 'Bạn có chắc chắn muốn xóa <Bold>{{title}}</Bold>?',
    },
    clearDialog: {
      title: 'Xóa TẤT CẢ?',
      content: 'Bạn có chắc chắn muốn xóa TẤT CẢ hội thoại không?',
    },
    languageDialog: {
      title: 'Chuyển ngôn ngữ',
    },
    feedbackDialog: {
      title: 'Phản hồi',
      content: 'Vui lòng cung cấp thêm chi tiết.',
      categoryLabel: 'Danh mục',
      commentLabel: 'Bình luận',
      commentPlaceholder: '(Tùy chọn) Nhập bình luận của bạn',
      categories: [
        {
          value: 'notFactuallyCorrect',
          label: 'Không chính xác',
        },
        {
          value: 'notFullyFollowRequest',
          label: 'Không hoàn toàn làm theo yêu cầu',
        },
        {
          value: 'other',
          label: 'Khác',
        },
      ],
    },
    button: {
      newChat: 'Hội thoại mới',
      botConsole: 'Bảng điều khiển Bot',
      sharedBotAnalytics: 'Phân tích Bot chia sẻ',
      apiManagement: 'Quản lý API',
      userUsages: 'Sử dụng của người dùng',
      SaveAndSubmit: 'Lưu và Gửi',
      resend: 'Gửi lại',
      regenerate: 'Tạo lại',
      delete: 'Xóa',
      deleteAll: 'Xóa tất cả',
      done: 'Xong',
      ok: 'OK',
      cancel: 'Hủy',
      back: 'Quay lại',
      menu: 'Menu',
      language: 'Ngôn ngữ',
      clearConversation: 'Xóa TẤT CẢ hội thoại',
      signOut: 'Đăng xuất',
      close: 'Đóng',
      add: 'Thêm',
      continue: 'Tiếp tục tạo',
    },
    error: {
      answerResponse: 'Đã xảy ra lỗi trong quá trình phản hồi.',
      notFoundPage: 'Không tìm thấy trang bạn đang tìm kiếm.',
    },
  },
};

export default translation;
