const translation = {
  translation: {
    app: {
      name: 'Bedrock Claude Chat',
      nameWithoutClaude: 'Bedrock Chat',
      inputMessage: 'Nachricht senden',
      starredBots: 'Favorisierte Bots',
      recentlyUsedBots: 'Zuletzt genutzte Bots',
      conversationHistory: 'Verlauf',
      chatWaitingSymbol: '▍',
    },
    bot: {
      label: {
        myBots: 'Meine Bots',
        recentlyUsedBots: 'Kürzlich genutzte Shared Bots',
        knowledge: 'Wissensbasis',
        url: 'URL',
        sitemap: 'Sitemap URL',
        file: 'Datei',
        loadingBot: 'Laden...',
        normalChat: 'Chat',
        notAvailableBot: '[NICHT Verfügbar]',
        notAvailableBotInputMessage: 'Dieser Bot ist NICHT verfügbar.',
        noDescription: 'Keine Beschreibung',
        notAvailable: 'Dieser Bot ist NICHT verfügbar.',
        noBots: 'Keine Bots.',
        noBotsRecentlyUsed: 'Keine kürzlich genutzen Shared Bots.',
        retrievingKnowledge: '[Retrieving Knowledge...]',
        dndFileUpload:
          'Sie können Dateien per Drag-and-Drop hochladen..\nUnterstützte Dateiformate: {{fileExtensions}}',
        uploadError: 'Fehler Nachricht',
        syncStatus: {
          queue: 'Warte auf Synchronisierung',
          running: 'Synchronisiere',
          success: 'Synchronisierung Erfolgreich',
          fail: 'Fehler bei der Synchronisierung',
        },
        fileUploadStatus: {
          uploading: 'Hochladen...',
          uploaded: 'Hochgeladen',
          error: 'ERROR',
        },
      },
      titleSubmenu: {
        edit: 'Editieren',
        copyLink: 'Link kopieren',
        copiedLink: 'Kopiert',
      },
      help: {
        overview:
          'Bots arbeiten nach vordefinierten Anweisungen. Normale Chats funktionieren nur wenn der komplette Kontext in der Nachricht definiert ist, aber bei Bots muss der Kontext nicht erneut definiert werden.',
        instructions:
          'Legen Sie fest, wie sich der Bot verhalten soll. Unklare Anweisungen können zu unerwünschten Ergebnissen führen, geben Sie also klare und präzise Anweisungen.',
        knowledge: {
          overview:
            'Indem man dem Bot eine externe Wissensbasis zur Verfügung stellt, wird er in die Lage versetzt, mit Daten umzugehen, für die er nicht vorher trainiert wurde.',
          url: 'Die Informationen aus der angegebenen URL werden als Wissensbasis verwendet.',
          sitemap:
            'Durch die Angabe der Sitemap URL werden die Informationen, die durch automatisches Scraping von Websites gewonnen werden, als Wissensbasis verwendet.',
          file: 'Die hochgeladenen Dateien werden als Wissensbasis verwendet.',
        },
      },
      alert: {
        sync: {
          error: {
            title: 'Wissensbasis Synchronisationsfehler',
            body: 'Bei der Synchronisierung der Wissensbasis ist ein Fehler aufgetreten. Bitte überprüfen Sie die folgende Meldung:',
          },
          incomplete: {
            title: 'NICHT bereit',
            body: 'Die Synchronisation der Wissensbasis ist noch NICHT abgeschlossen, daher wird die Wissensbasis vor der Aktualisierung verwendet.',
          },
        },
      },
      samples: {
        title: 'Beispiel Anweisungen',
        anthropicLibrary: {
          title: 'Anthropic Prompt Bibliothek',
          sentence: 'Benötigen Sie mehr Beispiele? Besuchen Sie: ',
          url: 'https://docs.anthropic.com/claude/prompt-library',
        },
        quizAssistant: {
          title: 'Quiz-Erstellungsassistent',
          prompt: `Sie sind ein hilfreicher KI-Assistent, der Lehrer bei der Erstellung von Quiz basierend auf Unterrichtsmaterialien unterstützt.
    Analysieren Sie die vom Benutzer bereitgestellte Beschreibung/Parameter und erstellen Sie dann ein Quiz basierend auf der Eingabe.
    
    Quiz-Parameter:
    -- Anzahl der Fragen (Standard: 10)
    -- Art des Quiz: Multiple Choice, Kurzantwort (Standard Multiple-Choice)
    -- Schwierigkeitsgrad der Fragen
    -- Quiz-Umfang:
    --- Dateiname(n), falls vorhanden
    --- Liste der Schwerpunktthemen
    --- Klassenstufe
    --- Nur Informationen aus der Wissensbasis verwenden oder allgemeines Wissen einbeziehen
    
    Quiz-Ausgabe:
    Für Fragen [1 bis N]
    Frage: Text
    Abgedecktes Konzept
    Zitation/Referenz zum Quellmaterial
    Multiple-Choice-Optionen
    Richtige Antwort - Schlüssel
    Analyse der Auswahlmöglichkeiten
    
    Wir möchten, dass der Quiz-Erstellungsprozess freundlich ist, und wenn der Benutzer nicht genügend Informationen bereitgestellt hat, fordern Sie den Benutzer auf, die notwendigen Details für das Quiz bereitzustellen. Stellen Sie sicher, dass Quellenangaben korrekt generiert werden.`
        },
        learningAssistant: {
          title: 'Mathematik-Lernassistent',
          prompt: `Sie sind ein Mathematik-Lehrassistent für die 8. Klasse, der Schüler und Lehrer bei der mathematischen Bildung unterstützt.
    Ihre Rolle beschränkt sich streng auf mathematische Themen, die den Standards der 8. Klasse entsprechen...`
        },
        pythonCodeAssistant: {
          title: 'Python Coding Assistent',
          prompt: `Schreiben Sie ein kurzes Python-Skript für die gestellte Aufgabe, wie es ein sehr erfahrener Python-Experte schreiben würde. Sie schreiben den Code für einen erfahrenen Entwickler, also fügen Sie nur Kommentare für Dinge hinzu, die nicht offensichtlich sind. Stellen Sie sicher, dass Sie alle erforderlichen Importe inkludieren.
Schreiben Sie NIEMALS etwas vor dem \`\`\`python\`\`\` block. Nachdem Sie den Code generiert haben und nach dem \`\`\`python\`\`\` block , überprüfen Sie Ihre Arbeit sorgfältig, um sicherzustellen, dass es keine Fehler, Irrtümer oder Unstimmigkeiten gibt. Wenn es Fehler gibt, listen Sie diese in <error>-Tags auf und erstellen Sie dann eine neue Version, in der die Fehler behoben sind. Wenn keine Fehler vorhanden sind, schreiben Sie "CHECKED: NO ERRORS" in die <error>-Tags.`,
        },
        mailCategorizer: {
          title: 'Mail-Kategorisierer',
          prompt: `Sie sind ein Kundendienstmitarbeiter, der die Aufgabe hat, E-Mails nach Typ zu klassifizieren. Bitte geben Sie Ihre Antwort aus und begründen Sie anschließend Ihre Klassifizierung.

Die Klassifizierungskategorien sind:
(A) Frage vor dem Verkauf
(B) Kaputter oder defekter Artikel
(C) Frage zur Rechnungsstellung
(D) Sonstiges (bitte erläutern)

Wie würden Sie diese E-Mail kategorisieren?`,
        },
        fitnessCoach: {
          title: 'Persönlicher Fitness-Trainer',
          prompt: `Sie sind ein fröhlicher, enthusiastischer Personal Fitness Coach namens Sam. Sam hilft seinen Kunden leidenschaftlich gern dabei, fit zu werden und einen gesünderen Lebensstil zu führen. Sie schreiben in einem ermutigenden und freundlichen Ton und versuchen immer, Ihre Kunden zu besseren Fitnesszielen zu führen. Wenn der Benutzer Sie etwas fragt, das nichts mit Fitness zu tun hat, bringen Sie das Thema entweder auf Fitness zurück oder sagen Sie, dass Sie nicht antworten können.`,
        },
      },
      create: {
        pageTitle: 'Meinen Bot erstellen',
      },
      edit: {
        pageTitle: 'Meinen Bot bearbeiten',
      },
      item: {
        title: 'Name',
        description: 'Beschreibung',
        instruction: 'Anweisungen',
      },
      button: {
        newBot: 'Neuen Bot erstellen',
        create: 'Erstellen',
        edit: 'Editieren',
        save: 'Speichern',
        delete: 'Löschen',
        share: 'Teilen',
        copy: 'Kopieren',
        copied: 'Kopiert',
        instructionsSamples: 'Beispiele',
        chooseFiles: 'Dateien auswählen',
      },
      deleteDialog: {
        title: 'Löschen?',
        content: 'Sind Sie sicher, dass Sie <Bold>{{Titel}}</Bold> löschen wollen?',
      },
      shareDialog: {
        title: 'Teilen',
        off: {
          content:
            'Die Freigabe von Links ist deaktiviert, so dass nur Sie über die URL auf diesen Bot zugreifen können.',
        },
        on: {
          content:
            'Die Linkfreigabe ist aktiviert, so dass ALLE Nutzer diesen Link zur Konversation nutzen können.',
        },
      },
      error: {
        notSupportedFile: 'Diese Datei wird nicht unterstützt.',
        duplicatedFile: 'Es wurde eine Datei mit demselben Namen hochgeladen.',
      },
    },
    deleteDialog: {
      title: 'Löschen?',
      content: 'Sind Sie sicher, dass Sie <Bold>{{Titel}}</Bold> löschen wollen?',
    },
    clearDialog: {
      title: 'ALLE Löschen?',
      content: 'Sind Sie sicher, dass Sie ALLE Chats löschen wollen?',
    },
    languageDialog: {
      title: 'Sprache ändern',
    },
    button: {
      newChat: 'Neuer Chat',
      botConsole: 'Bot Konsole',
      SaveAndSubmit: 'Speichern & Senden',
      resend: 'Eneut senden',
      regenerate: 'Erneut generieren',
      delete: 'Löschen',
      deleteAll: 'Alle löschen',
      done: 'Fertig',
      ok: 'OK',
      cancel: 'Abbrechen',
      back: 'Zurück',
      menu: 'Menü',
      language: 'Sprache',
      clearConversation: 'ALLE Chats löschen',
      signOut: 'Abmelden',
      close: 'Schließen',
      add: 'Hinzufügen',
      continue: 'Weiter generieren',
    },
    input: {
      hint: {
        required: '* Benötigt',
      },
    },
    error: {
      answerResponse: 'Bei der Beantwortung ist ein Fehler aufgetreten.',
      notFoundConversation:
        'Da der angegebene Chat nicht existiert, wird ein neuer Chat-Bildschirm angezeigt.',
      notFoundPage: 'Die von Ihnen gesuchte Seite wurde nicht gefunden.',
      predict: {
        general: 'Bei der Vorhersage ist ein Fehler aufgetreten.',
        invalidResponse:
          'Unerwartete Antwort erhalten. Das Antwortformat stimmt nicht mit dem erwarteten Format überein.',
      },
      notSupportedImage: 'Das ausgewählte Model unterstützt keine Bilder.',
    },
  },
};

export default translation;
