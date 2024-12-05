const translation = {
  translation: {
    signIn: {
      button: {
        login: 'Masuk',
      },
    },
    app: {
      name: 'Bedrock Claude Chat',
      nameWithoutClaude: 'Bedrock Chat',
      inputMessage: 'Bisakah Saya Membantu Anda?',
      starredBots: 'Bot Favorit',
      recentlyUsedBots: 'Bot yang Baru Digunakan',
      conversationHistory: 'Riwayat',
      chatWaitingSymbol: '▍',
      adminConsoles: 'Hanya Admin',
    },
    model: {
      haiku3: {
        label: 'Claude 3 (Haiku)',
        description:
          'Versi sebelumnya dioptimalkan untuk kecepatan dan kekompakan, memberikan respons hampir instan.',
      },
      sonnet3: {
        label: 'Claude 3 (Sonnet)',
        description: 'Keseimbangan antara kecerdasan dan kecepatan.',
      },
      'sonnet3-5': {
        label: 'Claude 3.5 (Sonnet) v1',
        description:
          'Versi awal dari Claude 3.5. Mendukung berbagai tugas, tetapi v2 menawarkan akurasi yang lebih baik.',
      },
      'sonnet3-5-v2': {
        label: 'Claude 3.5 (Sonnet) v2',
        description:
          'Versi terbaru dari Claude 3.5. Model yang ditingkatkan yang membangun dari v1 dengan akurasi dan performa yang lebih tinggi.',
      },
      'haiku3-5': {
        label: 'Claude 3.5 (Haiku)',
        description:
          'Versi terbaru, menawarkan respons yang lebih cepat dan kemampuan yang ditingkatkan dibandingkan Haiku 3.',
      },
      opus3: {
        label: 'Claude 3 (Opus)',
        description: 'Model yang kuat untuk tugas-tugas yang sangat kompleks.',
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
          'Model multimodal yang sangat mampu dengan kombinasi terbaik antara akurasi, kecepatan, dan biaya untuk berbagai macam tugas.',
      },
      novaLite: {
        label: 'Amazon Nova Lite',
        description:
          'Model multimodal dengan biaya sangat rendah yang sangat cepat dalam memproses input gambar, video, dan teks.',
      },
      novaMicro: {
        label: 'Amazon Nova Micro',
        description:
          'Model teks saja yang memberikan respons dengan latensi terendah dalam keluarga model Amazon Nova dengan biaya sangat rendah.',
      },
    },
    agent: {
      label: 'Agen',
      help: {
        overview:
          'Dengan menggunakan fungsionalitas Agen, chatbot Anda dapat secara otomatis menangani tugas-tugas yang lebih kompleks.',
      },
      hint: `Agen secara otomatis menentukan alat mana yang akan digunakan untuk menjawab pertanyaan pengguna. Karena waktu yang dibutuhkan untuk pengambilan keputusan, waktu respons cenderung lebih lama. Mengaktifkan satu atau lebih alat memungkinkan fungsionalitas agen. Sebaliknya, jika tidak ada alat yang dipilih, fungsionalitas agen tidak digunakan. Ketika fungsionalitas agen diaktifkan, penggunaan "Knowledge" juga diperlakukan sebagai salah satu alat. Ini berarti bahwa "Knowledge" mungkin tidak digunakan dalam respons.`,
      progress: {
        label: 'Berpikir...',
      },
      progressCard: {
        toolInput: 'Input: ',
        toolOutput: 'Output: ',
        status: {
          running: 'Sedang Berjalan...',
          success: 'Berhasil',
          error: 'Kesalahan',
        },
      },
      tools: {
        get_weather: {
          name: 'Cuaca Saat Ini',
          description: 'Mengambil prakiraan cuaca saat ini.',
        },
        sql_db_query: {
          name: 'Query Database',
          description:
            'Menjalankan query SQL yang detail dan benar untuk mengambil hasil dari database.',
        },
        sql_db_schema: {
          name: 'Skema Database',
          description: 'Mengambil skema dan sampel baris untuk daftar tabel.',
        },
        sql_db_list_tables: {
          name: 'Daftar Tabel Database',
          description: 'Daftar semua tabel yang tersedia di database.',
        },
        sql_db_query_checker: {
          name: 'Pemeriksa Query',
          description: 'Periksa apakah query SQL Anda benar sebelum eksekusi.',
        },
        internet_search: {
          name: 'Pencarian Internet',
          description: 'Mencari informasi di internet.',
        },
        knowledge_base_tool: {
          name: 'Ambil Pengetahuan',
          description: 'Mengambil informasi dari pengetahuan.',
        },
      },
    },
    bot: {
      label: {
        myBots: 'Bot Saya',
        recentlyUsedBots: 'Bot yang Baru Digunakan Bersama',
        knowledge: 'Pengetahuan',
        url: 'URL',
        s3url: 'Sumber Data S3',
        sitemap: 'URL Sitemap',
        file: 'File',
        loadingBot: 'Memuat...',
        normalChat: 'Chat',
        notAvailableBot: '[TIDAK tersedia]',
        notAvailableBotInputMessage: 'Bot ini TIDAK tersedia.',
        noDescription: 'Tanpa Deskripsi',
        notAvailable: 'Bot ini TIDAK tersedia.',
        noBots: 'Tidak Ada Bot.',
        noBotsRecentlyUsed: 'Tidak Ada Bot Bersama yang Baru Digunakan.',
        retrievingKnowledge: '[Mengambil Pengetahuan...]',
        selectParsingModel: 'Pilih Model Parsing',
        dndFileUpload:
          'Anda dapat mengunggah file dengan drag and drop.\nFile yang didukung: {{fileExtensions}}',
        uploadError: 'Pesan Kesalahan',
        referenceLink: 'Tautan Referensi',
        syncStatus: {
          queue: 'Menunggu Sinkronisasi',
          running: 'Sedang Sinkronisasi',
          success: 'Sinkronisasi Selesai',
          fail: 'Sinkronisasi Gagal',
        },
        fileUploadStatus: {
          uploading: 'Mengunggah...',
          uploaded: 'Diunggah',
          error: 'KESALAHAN',
        },
        quickStarter: {
          title: 'Pemula Cepat Percakapan',
          exampleTitle: 'Judul',
          example: 'Contoh Percakapan',
        },
        citeRetrievedContexts: 'Situmusi Konteks yang Diambil',
        unsupported: 'Tidak Didukung, Hanya Baca',
      },
      titleSubmenu: {
        edit: 'Edit',
        copyLink: 'Salin Tautan',
        copiedLink: 'Disalin',
      },
      help: {
        overview:
          'Bot beroperasi sesuai dengan instruksi yang telah ditetapkan. Chat tidak berfungsi sebagaimana mestinya kecuali konteks didefinisikan dalam pesan, tetapi dengan bot, tidak perlu mendefinisikan konteks.',
        instructions:
          'Tentukan bagaimana bot harus berperilaku. Memberikan instruksi yang ambigu dapat menyebabkan perilaku yang tidak dapat diprediksi, jadi berikan instruksi yang jelas dan spesifik.',
        knowledge: {
          overview:
            'Dengan menyediakan pengetahuan eksternal kepada bot, bot menjadi mampu menangani data yang tidak dilatih sebelumnya.',
          url: 'Informasi dari URL yang ditentukan akan digunakan sebagai Pengetahuan.',
          s3url:
            'Dengan memasukkan URI S3, Anda dapat menambahkan S3 sebagai sumber data. Anda dapat menambahkan hingga 4 sumber. Hanya mendukung bucket yang ada di akun dan wilayah bedrock yang sama.',
          sitemap:
            'Dengan menentukan URL sitemap, informasi yang diperoleh melalui pengikisan otomatis situs web di dalamnya akan digunakan sebagai Pengetahuan.',
          file: 'File yang diunggah akan digunakan sebagai Pengetahuan.',
          citeRetrievedContexts:
            'Konfigurasikan apakah akan menampilkan konteks yang diambil untuk menjawab pertanyaan pengguna sebagai informasi sitasi.\nJika diaktifkan, pengguna dapat mengakses URL sumber asli atau file.',
        },
        quickStarter: {
          overview:
            'Saat memulai percakapan, berikan contoh. Contoh menggambarkan cara menggunakan bot.',
        },
      },
      alert: {
        sync: {
          error: {
            title: 'Kesalahan Sinkronisasi Pengetahuan',
            body: 'Terjadi kesalahan saat menyinkronkan Pengetahuan. Silakan periksa pesan berikut:',
          },
          incomplete: {
            title: 'TIDAK Siap',
            body: 'Bot ini belum menyelesaikan sinkronisasi pengetahuan, jadi pengetahuan sebelum pembaruan digunakan.',
          },
        },
      },
      samples: {
        title: 'Contoh Instruksi',
        anthropicLibrary: {
          title: 'Perpustakaan Prompt Antropik',
          sentence: 'Apakah Anda memerlukan lebih banyak contoh? Kunjungi: ',
          url: 'https://docs.anthropic.com/claude/prompt-library',
        },
        pythonCodeAssistant: {
          title: 'Asisten Kode Python',
          prompt: `Tulis skrip python yang singkat dan berkualitas tinggi untuk tugas yang diberikan, sesuatu yang akan ditulis oleh ahli python yang sangat terampil. Anda menulis kode untuk pengembang berpengalaman sehingga hanya menambahkan komentar untuk hal-hal yang tidak jelas. Pastikan untuk menyertakan impor yang diperlukan. 
    JANGAN PERNAH menulis apa pun sebelum blok \`\`\`python\`\`\`. Setelah Anda selesai menghasilkan kode dan setelah blok \`\`\`python\`\`\`, periksa pekerjaan Anda dengan hati-hati untuk memastikan tidak ada kesalahan, error, atau inkonsistensi. Jika ada kesalahan, daftarkan kesalahan tersebut dalam tag <error>, lalu hasilkan versi baru dengan kesalahan tersebut diperbaiki. Jika tidak ada kesalahan, tulis "DI CEK: TIDAK ADA KESALAHAN" dalam tag <error>.`,
        },
        mailCategorizer: {
          title: 'Kategorizer Mail',
          prompt: `Anda adalah agen layanan pelanggan yang ditugaskan untuk mengklasifikasikan email berdasarkan jenisnya. Harap keluarkan jawaban Anda dan kemudian jelaskan klasifikasi Anda. 
    
    Kategori klasifikasi adalah: 
    (A) Pertanyaan pra-penjualan 
    (B) Barang rusak atau cacat 
    (C) Pertanyaan penagihan 
    (D) Lainnya (harap jelaskan)
    
    Bagaimana Anda akan mengkategorikan email ini?`,
        },
        fitnessCoach: {
          title: 'Pelatih Kebugaran Pribadi',
          prompt: `Anda adalah pelatih kebugaran pribadi yang ceria dan antusias bernama Sam. Sam bersemangat membantu klien menjadi bugar dan menjalani gaya hidup yang lebih sehat. Anda menulis dengan nada yang mendukung dan ramah serta selalu berusaha membimbing klien Anda menuju tujuan kebugaran yang lebih baik. Jika pengguna bertanya sesuatu yang tidak terkait dengan kebugaran, bawa topik kembali ke kebugaran, atau katakan bahwa Anda tidak dapat menjawab.`,
        },
      },
      create: {
        pageTitle: 'Buat Bot Saya',
      },
      edit: {
        pageTitle: 'Edit Bot Saya',
      },

      item: {
        title: 'Nama',
        description: 'Deskripsi',
        instruction: 'Instruksi',
      },
      explore: {
        label: {
          pageTitle: 'Konsol Bot',
        },
      },
      apiSettings: {
        pageTitle: 'Pengaturan API Publikasi Bot Bersama',
        label: {
          endpoint: 'Endpoint API',
          usagePlan: 'Rencana Penggunaan',
          allowOrigins: 'Asal yang Diizinkan',
          apiKeys: 'Kunci API',
          period: {
            day: 'Per HARI',
            week: 'Per MINGGU',
            month: 'Per BULAN',
          },
          apiKeyDetail: {
            creationDate: 'Tanggal Pembuatan',
            active: 'Aktif',
            inactive: 'Tidak Aktif',
            key: 'Kunci API',
          },
        },
        item: {
          throttling: 'Pembatasan',
          burstLimit: 'Burst',
          rateLimit: 'Batas Kecepatan',
          quota: 'Kuota',
          requestLimit: 'Permintaan',
          offset: 'Offset',
        },
        help: {
          overview:
            'Membuat API memungkinkan fungsi Bot diakses oleh klien eksternal; API memungkinkan integrasi dengan aplikasi eksternal.',
          endpoint: 'Klien dapat menggunakan Bot dari endpoint ini.',
          usagePlan:
            'Rencana penggunaan menentukan jumlah atau laju permintaan yang diterima API Anda dari klien. Kaitkan API dengan rencana penggunaan untuk melacak permintaan yang diterima API Anda.',
          throttling: 'Batasi laju pengguna dapat memanggil API Anda.',
          rateLimit:
            'Masukkan laju, dalam permintaan per detik, yang dapat dipanggil klien ke API Anda.',
          burstLimit:
            'Masukkan jumlah permintaan bersamaan yang dapat dibuat klien ke API Anda.',
          quota:
            'Aktifkan kuota untuk membatasi jumlah permintaan yang dapat dilakukan pengguna ke API Anda dalam periode waktu tertentu.',
          requestLimit:
            'Masukkan jumlah total permintaan yang dapat dilakukan pengguna dalam periode waktu yang Anda pilih di daftar dropdown.',
          allowOrigins:
            'Asal klien yang diizinkan untuk akses. Jika asal tidak diizinkan, pemanggil menerima respons 403 Forbidden dan ditolak akses ke API. Origin harus mengikuti format: "(http|https)://nama-host" atau "(http|https)://nama-host:port" dan wildcard (*) dapat digunakan.',
          allowOriginsExample:
            'mis. https://your-host-name.com, https://*.your-host-name.com, http://localhost:8000',
          apiKeys:
            'Kunci API adalah string alfanumerik yang digunakan untuk mengidentifikasi klien API Anda. Jika tidak, pemanggil menerima respons 403 Forbidden dan ditolak akses ke API.',
        },
        button: {
          ApiKeyShow: 'Tampilkan',
          ApiKeyHide: 'Sembunyikan',
        },
        alert: {
          botUnshared: {
            title: 'Silakan Bagikan Bot',
            body: 'Anda tidak dapat menerbitkan API untuk bot yang tidak dibagikan.',
          },
          deploying: {
            title: 'Deployment API sedang BERLANGSUNG',
            body: 'Harap tunggu hingga deployment selesai.',
          },
          deployed: {
            title: 'API telah DIPUBLIKASIKAN',
            body: 'Anda dapat mengakses API dari Klien menggunakan Endpoint API dan Kunci API.',
          },
          deployError: {
            title: 'GAGAL menerbitkan API',
            body: 'Silakan hapus API dan buat ulang API.',
          },
        },
        deleteApiDaialog: {
          title: 'Hapus?',
          content:
            'Apakah Anda yakin ingin menghapus API? Endpoint API akan dihapus, dan klien tidak akan lagi memiliki akses ke dalamnya.',
        },
        addApiKeyDialog: {
          title: 'Tambah Kunci API',
          content: 'Masukkan nama untuk mengidentifikasi Kunci API.',
        },
        deleteApiKeyDialog: {
          title: 'Hapus?',
          content:
            'Apakah Anda yakin ingin menghapus <Bold>{{title}}</Bold>?\nKlien yang menggunakan Kunci API ini akan ditolak akses ke API.',
        },
      },
      button: {
        newBot: 'Buat Bot Baru',
        create: 'Buat',
        edit: 'Edit',
        delete: 'Hapus',
        share: 'Bagikan',
        apiSettings: 'Pengaturan Publikasi API',
        copy: 'Salin',
        copied: 'Disalin',
        instructionsSamples: 'Contoh',
        chooseFiles: 'Pilih file',
      },
      deleteDialog: {
        title: 'Hapus?',
        content: 'Apakah Anda yakin ingin menghapus <Bold>{{title}}</Bold>?',
      },
      shareDialog: {
        title: 'Bagikan',
        off: {
          content:
            'Pembagian tautan dimatikan, jadi hanya Anda yang dapat mengakses bot ini melalui URL-nya.',
        },
        on: {
          content:
            'Pembagian tautan diaktifkan, jadi SEMUA pengguna dapat menggunakan tautan ini untuk percakapan.',
        },
      },
      error: {
        notSupportedFile: 'File ini tidak didukung.',
        duplicatedFile: 'File dengan nama yang sama telah diunggah.',
        failDeleteApi: 'Gagal menghapus API.',
      },
    },
    admin: {
      sharedBotAnalytics: {
        label: {
          pageTitle: 'Analitik Bot Bersama',
          noPublicBotUsages:
            'Selama Periode Perhitungan, tidak ada bot publik yang digunakan.',
          published: 'API telah diterbitkan.',
          SearchCondition: {
            title: 'Periode Perhitungan',
            from: 'Dari',
            to: 'Ke',
          },
          sortByCost: 'Urutkan berdasarkan Biaya',
        },
        help: {
          overview:
            'Pantau status penggunaan Bot Bersama dan API Bot yang Diterbitkan.',
          calculationPeriod:
            'Jika Periode Perhitungan tidak diatur, biaya untuk hari ini akan ditampilkan.',
        },
      },
      apiManagement: {
        label: {
          pageTitle: 'Manajemen API',
          publishedDate: 'Tanggal Diterbitkan',
          noApi: 'Tidak Ada API.',
        },
      },
      botManagement: {
        label: {
          pageTitle: 'Manajemen Bot',
          sharedUrl: 'URL Bot Bersama',
          apiSettings: 'Pengaturan Publikasi API',
          noKnowledge: 'Bot ini tidak memiliki Pengetahuan.',
          notPublishApi: 'API bot ini belum diterbitkan.',
          deployStatus: 'Status Deployment',
          cfnStatus: 'Status CloudFormation',
          codebuildStatus: 'Status CodeBuild',
          codeBuildId: 'ID CodeBuild',
          usagePlanOn: 'NYALA',
          usagePlanOff: 'MATI',
          rateLimit:
            '<Bold>{{limit}}</Bold> permintaan per detik, yang dapat dipanggil klien ke API.',
          burstLimit:
            'Klien dapat melakukan <Bold>{{limit}}</Bold> permintaan bersamaan ke API.',
          requestsLimit:
            'Anda dapat melakukan <Bold>{{limit}}</Bold> permintaan <Bold>{{period}}</Bold>.',
        },
        alert: {
          noApiKeys: {
            title: 'Tidak Ada Kunci API',
            body: 'Semua klien tidak dapat mengakses API.',
          },
        },
        button: {
          deleteApi: 'Hapus API',
        },
      },
      validationError: {
        period: 'Masukkan baik Dari dan Ke',
      },
    },
    deleteDialog: {
      title: 'Hapus?',
      content: 'Apakah Anda yakin ingin menghapus <Bold>{{title}}</Bold>?',
    },
    clearDialog: {
      title: 'Hapus SEMUA?',
      content: 'Apakah Anda yakin ingin menghapus SEMUA percakapan?',
    },
    languageDialog: {
      title: 'Ganti Bahasa',
    },
    feedbackDialog: {
      title: 'Umpan Balik',
      content: 'Silakan berikan detail lebih lanjut.',
      categoryLabel: 'Kategori',
      commentLabel: 'Komentar',
      commentPlaceholder: '(Opsional) Masukkan komentar Anda',
      categories: [
        {
          value: 'notFactuallyCorrect',
          label: 'Tidak Faktual',
        },
        {
          value: 'notFullyFollowRequest',
          label: 'Tidak Sepenuhnya Mengikuti Permintaan Saya',
        },
        {
          value: 'other',
          label: 'Lainnya',
        },
      ],
    },
    button: {
      newChat: 'Chat Baru',
      botConsole: 'Konsol Bot',
      sharedBotAnalytics: 'Analitik Bot Bersama',
      apiManagement: 'Manajemen API',
      userUsages: 'Penggunaan Pengguna',
      SaveAndSubmit: 'Simpan & Kirim',
      resend: 'Kirim Ulang',
      regenerate: 'Regenerasi',
      delete: 'Hapus',
      deleteAll: 'Hapus Semua',
      done: 'Selesai',
      ok: 'OK',
      cancel: 'Batal',
      back: 'Kembali',
      menu: 'Menu',
      language: 'Bahasa',
      clearConversation: 'Hapus SEMUA percakapan',
      signOut: 'Keluar',
      close: 'Tutup',
      add: 'Tambah',
      continue: 'Lanjutkan untuk menghasilkan',
    },
    input: {
      hint: {
        required: '* Wajib diisi',
      },
      validationError: {
        required: 'Field ini wajib diisi.',
        invalidOriginFormat: 'Format Origin tidak valid.',
      },
    },
    embeddingSettings: {
      title: 'Pengaturan Embedding',
      description:
        'Anda dapat mengonfigurasi parameter untuk vektor embeddings. Dengan menyesuaikan parameter, Anda dapat mengubah akurasi pengambilan dokumen.',
      chunkSize: {
        label: 'ukuran potongan',
        hint: 'Ukuran potongan mengacu pada ukuran di mana dokumen dibagi menjadi segmen yang lebih kecil',
      },
      chunkOverlap: {
        label: 'tumpang tindih potongan',
        hint: 'Anda dapat menentukan jumlah karakter yang tumpang tindih antara potongan yang bersebelahan.',
      },
      enablePartitionPdf: {
        label:
          'Aktifkan analisis PDF terperinci. Jika diaktifkan, PDF akan dianalisis secara mendetail seiring waktu.',
        hint: 'Efektif ketika Anda ingin meningkatkan akurasi pencarian. Biaya komputasi meningkat karena komputasi membutuhkan lebih banyak waktu.',
      },
      help: {
        chunkSize:
          'Ketika ukuran potongan terlalu kecil, informasi kontekstual bisa hilang, dan ketika terlalu besar, informasi kontekstual yang berbeda mungkin ada dalam potongan yang sama, yang berpotensi mengurangi akurasi pencarian.',
        chunkOverlap:
          'Dengan menentukan tumpang tindih potongan, Anda dapat mempertahankan informasi kontekstual di sekitar batas potongan. Meningkatkan ukuran potongan kadang-kadang dapat meningkatkan akurasi pencarian. Namun, perlu diingat bahwa meningkatkan tumpang tindih potongan dapat menyebabkan biaya komputasi yang lebih tinggi.',
        overlapTokens:
          'Anda mengonfigurasi jumlah token yang akan tumpang tindih, atau diulang di seluruh potongan yang bersebelahan. Misalnya, jika Anda mengatur token tumpang tindih menjadi 60, 60 token terakhir di potongan pertama juga termasuk di awal potongan kedua.',
        maxParentTokenSize:
          'Anda dapat menentukan ukuran token induk. Selama pengambilan, sistem awalnya mengambil potongan anak, tetapi menggantinya dengan potongan induk yang lebih luas agar model memiliki konteks yang lebih komprehensif',
        maxChildTokenSize:
          'Anda dapat menentukan ukuran token anak. Selama pengambilan, sistem awalnya mengambil potongan anak, tetapi menggantinya dengan potongan induk yang lebih luas agar model memiliki konteks yang lebih komprehensif',
        bufferSize:
          'Parameter ini dapat mempengaruhi seberapa banyak teks yang diperiksa bersama untuk menentukan batas setiap potongan, mempengaruhi granularitas dan koherensi potongan yang dihasilkan. Ukuran buffer yang lebih besar mungkin menangkap lebih banyak konteks tetapi juga dapat memperkenalkan noise, sementara ukuran buffer yang lebih kecil mungkin kehilangan konteks penting tetapi memastikan pemotongan yang lebih tepat.',
        breakpointPercentileThreshold:
          'Ambang batas persentil yang lebih tinggi mengharuskan kalimat untuk lebih dapat dibedakan agar dapat dipisahkan menjadi potongan yang berbeda. Ambang batas yang lebih tinggi menghasilkan lebih sedikit potongan dan biasanya ukuran potongan rata-rata yang lebih besar.',
      },
      alert: {
        sync: {
          error: {
            title: 'Kesalahan Pemisah Kalimat',
            body: 'Coba lagi dengan nilai tumpang tindih potongan yang lebih kecil',
          },
        },
      },
    },
    generationConfig: {
      title: 'Konfigurasi Generasi',
      description:
        'Anda dapat mengonfigurasi parameter inferensi LLM untuk mengontrol respons dari model.',
      maxTokens: {
        label: 'Panjang generasi maksimum/token baru maksimum',
        hint: 'Jumlah maksimum token yang diizinkan dalam respons yang dihasilkan',
      },
      temperature: {
        label: 'Temperatur',
        hint: 'Mempengaruhi bentuk distribusi probabilitas untuk output yang diprediksi dan mempengaruhi kemungkinan model memilih output dengan probabilitas lebih rendah',
        help: 'Pilih nilai yang lebih rendah untuk mempengaruhi model memilih output dengan probabilitas lebih tinggi; Pilih nilai yang lebih tinggi untuk mempengaruhi model memilih output dengan probabilitas lebih rendah',
      },
      topK: {
        label: 'Top-k',
        hint: 'Jumlah kandidat paling mungkin yang dipertimbangkan model untuk token berikutnya',
        help: 'Pilih nilai yang lebih rendah untuk mengurangi ukuran kumpulan dan membatasi opsi ke output yang lebih mungkin; Pilih nilai yang lebih tinggi untuk meningkatkan ukuran kumpulan dan memungkinkan model mempertimbangkan output yang kurang mungkin',
      },
      topP: {
        label: 'Top-p',
        hint: 'Persentase kandidat paling mungkin yang dipertimbangkan model untuk token berikutnya',
        help: 'Pilih nilai yang lebih rendah untuk mengurangi ukuran kumpulan dan membatasi opsi ke output yang lebih mungkin; Pilih nilai yang lebih tinggi untuk meningkatkan ukuran kumpulan dan memungkinkan model mempertimbangkan output yang kurang mungkin',
      },
      stopSequences: {
        label: 'Token akhir/urutan akhir',
        hint: 'Tentukan urutan karakter yang menghentikan model dari menghasilkan token lebih lanjut. Gunakan koma untuk memisahkan beberapa kata',
      },
    },
    searchSettings: {
      title: 'Pengaturan Pencarian',
      description:
        'Anda dapat mengonfigurasi parameter pencarian untuk mengambil dokumen yang relevan dari penyimpanan vektor.',
      maxResults: {
        label: 'Hasil Maksimum',
        hint: 'Jumlah maksimum catatan yang diambil dari penyimpanan vektor',
      },
      searchType: {
        label: 'Jenis Pencarian',
        hybrid: {
          label: 'Pencarian hybrid',
          hint: 'Menggabungkan skor relevansi dari pencarian semantik dan teks untuk memberikan akurasi yang lebih besar.',
        },
        semantic: {
          label: 'Pencarian semantik',
          hint: 'Menggunakan embeddings vektor untuk memberikan hasil yang relevan.',
        },
      },
    },
    knowledgeBaseSettings: {
      title: 'Pengaturan Detail Pengetahuan',
      description:
        'Pilih model embedded untuk mengonfigurasi pengetahuan, dan atur metode untuk membagi dokumen yang ditambahkan sebagai pengetahuan. Pengaturan ini tidak dapat diubah setelah membuat bot.',
      embeddingModel: {
        label: 'Model Embeddings',
        titan_v2: {
          label: 'Titan Embedding Text v2',
        },
        cohere_multilingual_v3: {
          label: 'Embed Multilingual v3',
        },
      },
      chunkingStrategy: {
        label: 'Strategi Pemotongan',
        default: {
          label: 'pemotongan default',
          hint: 'Secara otomatis membagi teks menjadi potongan sekitar 300 token secara default. Jika dokumen kurang dari atau sudah 300 token, tidak akan dipotong lagi.',
        },
        fixed_size: {
          label: 'pemotongan ukuran tetap',
          hint: 'Membagi teks menjadi ukuran token yang kira-kira ditetapkan.',
        },
        hierarchical: {
          label: 'pemotongan hierarkis',
          hint: 'Membagi teks menjadi struktur bersarang dari potongan anak dan induk.',
        },
        semantic: {
          label: 'pemotongan semantik',
          hint: 'Membagi teks menjadi potongan bermakna untuk meningkatkan pemahaman dan pengambilan informasi.',
        },
        none: {
          label: 'Tidak ada pemotongan',
          hint: 'Dokumen tidak akan dibagi.',
        },
      },
      chunkingMaxTokens: {
        label: 'Token Maksimum',
        hint: 'Jumlah maksimum token per potongan',
      },
      chunkingOverlapPercentage: {
        label: 'Persentase Tumpang Tindih antara Potongan',
        hint: 'Tumpang tindih potongan induk tergantung pada ukuran token anak dan persentase tumpang tindih anak yang Anda tentukan.',
      },
      overlapTokens: {
        label: 'Token Tumpang Tindih',
        hint: 'Jumlah token yang diulang di seluruh potongan dalam lapisan yang sama',
      },
      maxParentTokenSize: {
        label: 'Ukuran Token Induk Maksimum',
        hint: 'Jumlah maksimum token yang dapat dimiliki potongan dalam lapisan Induk',
      },
      maxChildTokenSize: {
        label: 'Ukuran Token Anak Maksimum',
        hint: 'Jumlah maksimum token yang dapat dimiliki potongan dalam lapisan Anak',
      },
      bufferSize: {
        label: 'Ukuran Buffer',
        hint: 'jumlah kalimat sekitar yang akan ditambahkan untuk pembuatan embeddings. Ukuran buffer 1 menghasilkan 3 kalimat (kalimat saat ini, kalimat sebelumnya, dan kalimat berikutnya) yang digabungkan dan di-embed',
      },
      breakpointPercentileThreshold: {
        label: 'Ambang Batas Persentil Breakpoint',
        hint: 'Ambang batas persentil jarak/kesenjangan kalimat untuk menggambar breakpoint antara kalimat.',
      },
      opensearchAnalyzer: {
        label: 'Analyzer (Tokenisasi, Normalisasi)',
        hint: 'Anda dapat menentukan analyzer untuk tokenisasi dan normalisasi dokumen yang terdaftar sebagai pengetahuan. Memilih analyzer yang sesuai akan meningkatkan akurasi pencarian. Silakan pilih analyzer optimal yang sesuai dengan bahasa pengetahuan Anda.',
        icu: {
          label: 'ICU analyzer',
          hint: 'Untuk tokenisasi, {{tokenizer}} digunakan, dan untuk normalisasi, {{normalizer}} digunakan.',
        },
        kuromoji: {
          label: 'Japanese (kuromoji) analyzer',
          hint: 'Untuk tokenisasi, {{tokenizer}} digunakan, dan untuk normalisasi, {{normalizer}} digunakan.',
        },
        none: {
          label: 'Analyzer default sistem',
          hint: 'Analyzer default yang ditentukan oleh sistem (OpenSearch) akan digunakan.',
        },
        tokenizer: 'Tokenizer:',
        normalizer: 'Normalizer:',
        token_filter: 'Token Filter:',
        not_specified: 'Tidak ditentukan',
      },
      advancedParsing: {
        label: 'Parsing Lanjutan',
        description:
          'Pilih model untuk digunakan dalam kemampuan parsing dokumen lanjutan.',
        hint: 'Cocok untuk parsing lebih dari teks standar dalam format dokumen yang didukung, termasuk tabel dalam PDF dengan struktur tetap. Biaya tambahan dikenakan untuk parsing menggunakan AI generatif.',
      },
      parsingModel: {
        label: 'Model Parsing Lanjutan',
        none: {
          label: 'Dinonaktifkan',
          hint: 'Tidak ada parsing lanjutan yang akan diterapkan.',
        },
        claude_3_sonnet_v1: {
          label: 'Claude 3 Sonnet v1',
          hint: 'Gunakan Claude 3 Sonnet v1 untuk parsing dokumen lanjutan.',
        },
        claude_3_haiku_v1: {
          label: 'Claude 3 Haiku v1',
          hint: 'Gunakan Claude 3 Haiku v1 untuk parsing dokumen lanjutan.',
        },
      },
      webCrawlerConfig: {
        title: 'Konfigurasi Web Crawler',
        crawlingScope: {
          label: 'Lingkup Pengikisan',
          default: {
            label: 'Default',
            hint: 'Batasi pengikisan ke halaman web yang termasuk dalam host yang sama dan dengan jalur URL awal yang sama. Misalnya, dengan seed URL "https://aws.amazon.com/bedrock/" maka hanya jalur ini dan halaman web yang memperluas jalur ini yang akan diikis, seperti "https://aws.amazon.com/bedrock/agents/". URL saudara seperti "https://aws.amazon.com/ec2/" tidak diikis, misalnya.',
          },
          subdomains: {
            label: 'Subdomain',
            hint: 'Sertakan pengikisan halaman web apa pun yang memiliki domain utama yang sama dengan seed URL. Misalnya, dengan seed URL "https://aws.amazon.com/bedrock/" maka halaman web apa pun yang mengandung "amazon.com" akan diikis, seperti "https://www.amazon.com".',
          },
          hostOnly: {
            label: 'Hanya Host',
            hint: 'Batasi pengikisan ke halaman web yang termasuk dalam host yang sama. Misalnya, dengan seed URL "https://aws.amazon.com/bedrock/", maka halaman web dengan "https://docs.aws.amazon.com" juga akan diikis, seperti "https://aws.amazon.com/ec2".',
          },
        },
        includePatterns: {
          label: 'Pola yang Disertakan',
          hint: 'Tentukan pola yang akan disertakan dalam pengikisan web. Hanya URL yang cocok dengan pola ini yang akan diikis.',
        },
        excludePatterns: {
          label: 'Pola yang Dikecualikan',
          hint: 'Tentukan pola yang akan dikecualikan dari pengikisan web. URL yang cocok dengan pola ini tidak akan diikis.',
        },
      },
    },
    error: {
      answerResponse: 'Terjadi kesalahan saat merespons.',
      notFoundConversation:
        'Karena chat yang ditentukan tidak ada, layar chat baru ditampilkan.',
      notFoundPage: 'Halaman yang Anda cari tidak ditemukan.',
      unexpectedError: {
        title: 'Terjadi kesalahan yang tidak terduga.',
        restore: 'Kembali ke halaman UTAMA',
      },
      predict: {
        general: 'Terjadi kesalahan saat memprediksi.',
        invalidResponse:
          'Respons yang tidak terduga diterima. Format respons tidak sesuai dengan format yang diharapkan.',
      },
      notSupportedImage: 'Model yang dipilih tidak mendukung gambar.',
      unsupportedFileFormat: 'Format file yang dipilih tidak didukung.',
      totalFileSizeToSendExceeded:
        'Ukuran total file harus tidak lebih dari {{maxSize}}.',
      attachment: {
        fileSizeExceeded:
          'Ukuran setiap dokumen harus tidak lebih dari {{maxSize}}.',
        fileCountExceeded:
          'Tidak dapat mengunggah lebih dari {{maxCount}} file.',
      },
    },
    validation: {
      title: 'Kesalahan Validasi',
      maxRange: {
        message: 'Nilai maksimum yang dapat diatur adalah {{size}}',
      },
      minRange: {
        message: 'Nilai minimum yang dapat diatur adalah {{size}}',
      },
      chunkOverlapLessThanChunkSize: {
        message:
          'Tumpang tindih potongan harus diatur kurang dari ukuran potongan',
      },
      parentTokenRange: {
        message: 'Ukuran token induk harus lebih besar dari ukuran token anak',
      },
      quickStarter: {
        message: 'Silakan masukkan baik Judul maupun Contoh Percakapan.',
      },
    },
    helper: {
      shortcuts: {
        title: 'Shortcut Keys',
        items: {
          focusInput: 'Geser fokus ke input chat',
          newChat: 'Buka chat baru',
        },
      },
    },
    guardrails: {
      title: 'Guardrails',
      label: 'Aktifkan Guardrails untuk Amazon Bedrock',
      hint: 'Guardrails untuk Amazon Bedrock digunakan untuk menerapkan pengaman khusus aplikasi berdasarkan kasus penggunaan Anda dan kebijakan AI bertanggung jawab.',
      harmfulCategories: {
        label: 'Kategori Berbahaya',
        hint: 'Konfigurasikan filter konten dengan menyesuaikan tingkat penyaringan untuk mendeteksi dan memblokir input pengguna yang berbahaya dan respons model yang melanggar kebijakan penggunaan Anda. 0: nonaktifkan, 1: rendah, 2: sedang, 3: tinggi',
        hate: {
          label: 'Hate',
          hint: 'Menggambarkan prompt input dan respons model yang mendiskriminasi, mengkritik, menghina, mengecam, atau mendehumanisasi seseorang atau kelompok berdasarkan identitas (seperti ras, etnis, gender, agama, orientasi seksual, kemampuan, dan asal negara). 0: nonaktifkan, 1: rendah, 2: sedang, 3: tinggi',
        },
        insults: {
          label: 'Insult',
          hint: 'Menggambarkan prompt input dan respons model yang mencakup bahasa yang merendahkan, memalukan, mengejek, menghina, atau meremehkan. Jenis bahasa ini juga diberi label sebagai bullying. 0: nonaktifkan, 1: rendah, 2: sedang, 3: tinggi',
        },
        sexual: {
          label: 'Seksual',
          hint: 'Menggambarkan prompt input dan respons model yang menunjukkan minat seksual, aktivitas, atau gairah menggunakan referensi langsung atau tidak langsung ke bagian tubuh, ciri fisik, atau seks. 0: nonaktifkan, 1: rendah, 2: sedang, 3: tinggi',
        },
        violence: {
          label: 'Kekerasan',
          hint: 'Menggambarkan prompt input dan respons model yang mencakup glorifikasi atau ancaman untuk menyebabkan rasa sakit fisik, melukai, atau cedera terhadap seseorang, kelompok, atau sesuatu. 0: nonaktifkan, 1: rendah, 2: sedang, 3: tinggi',
        },
        misconduct: {
          label: 'Perilaku Buruk',
          hint: 'Menggambarkan prompt input dan respons model yang mencari atau memberikan informasi tentang keterlibatan dalam aktivitas yang salah, atau mencelakai, menipu, atau memanfaatkan seseorang, kelompok, atau institusi. 0: nonaktifkan, 1: rendah, 2: sedang, 3: tinggi',
        },
      },
      promptAttacks: {
        hint: 'Menggambarkan prompt pengguna yang dimaksudkan untuk melewati kemampuan keamanan dan moderasi dari model dasar untuk menghasilkan konten berbahaya (juga dikenal sebagai jailbreak), dan mengabaikan serta menimpa instruksi yang ditentukan oleh pengembang (disebut injeksi prompt). Silakan merujuk ke Serangan Prompt untuk lebih banyak detail untuk menggunakannya dengan penandaan input.',
      },
      deniedTopics: {
        hint: 'Tambahkan hingga 30 topik yang dilarang untuk memblokir input pengguna atau respons model yang terkait dengan topik tersebut.',
      },
      wordFilters: {
        hint: 'Gunakan filter ini untuk memblokir kata dan frasa tertentu dalam input pengguna dan respons model.',
        profanityFilter: {
          hint: 'Aktifkan fitur ini untuk memblokir kata-kata kasar dalam input pengguna dan respons model. Daftar kata didasarkan pada definisi profanitas global dan dapat berubah.',
        },
        customWordsAndPhrases: {
          hint: 'Tentukan hingga 10.000 kata atau frasa (maks. 3 kata) yang akan diblokir oleh guardrail. Pesan yang diblokir akan ditampilkan jika input pengguna atau respons model mengandung kata atau frasa tersebut.',
        },
      },
      sensitiveInformationFilters: {
        hint: 'Gunakan filter ini untuk menangani data apa pun yang terkait dengan privasi.',
        personallyIdentifiableInformationTypes: {
          PIITypes: {},
          regexPatterns: {},
        },
      },
      contextualGroundingCheck: {
        label: 'Pemeriksaan Grounding Kontekstual',
        hint: 'Gunakan kebijakan ini untuk memvalidasi apakah respons model didasarkan pada sumber referensi dan relevan dengan pertanyaan pengguna untuk menyaring halusinasi model.',
        groundingThreshold: {
          label: 'Grounding',
          hint: 'Validasi apakah respons model didasarkan dan faktual berdasarkan informasi yang diberikan dalam sumber referensi, dan blok respons yang berada di bawah ambang batas grounding yang ditentukan. 0: tidak memblokir apa pun, 0.99: memblokir hampir semuanya',
        },
        relevanceThreshold: {
          label: 'Relevansi',
          hint: 'Validasi apakah respons model relevan dengan pertanyaan pengguna dan blok respons yang berada di bawah ambang batas relevansi yang ditentukan. 0: tidak memblokir apa pun, 0.99: memblokir hampir semuanya',
        },
      },
    },
  },
};

export default translation;
