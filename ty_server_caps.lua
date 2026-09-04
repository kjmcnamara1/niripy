{
  codeActionProvider = {
    codeActionKinds = { "quickfix" }
  },
  completionProvider = {
    triggerCharacters = { "." }
  },
  declarationProvider = true,
  definitionProvider = true,
  diagnosticProvider = {
    identifier = "ty",
    interFileDependencies = true,
    workDoneProgress = true,
    workspaceDiagnostics = true
  },
  documentHighlightProvider = true,
  documentSymbolProvider = true,
  executeCommandProvider = {
    commands = { "ty.printDebugInformation" },
    workDoneProgress = false
  },
  foldingRangeProvider = true,
  hoverProvider = true,
  inlayHintProvider = vim.empty_dict(),
  notebookDocumentSync = {
    notebookSelector = { {
        cells = { {
            language = "python"
          } }
      } },
    save = false
  },
  positionEncoding = "utf-8",
  referencesProvider = true,
  renameProvider = {
    prepareProvider = true
  },
  selectionRangeProvider = true,
  semanticTokensProvider = {
    full = true,
    legend = {
      tokenModifiers = { "definition", "readonly", "async", "documentation" },
      tokenTypes = { "namespace", "class", "parameter", "selfParameter", "clsParameter", "variable", "property", "function", "method", "keyword", "string", "number", "decorator", "builtinConstant", "typeParameter" }
    },
    range = true
  },
  signatureHelpProvider = {
    retriggerCharacters = { ")" },
    triggerCharacters = { "(", "," }
  },
  textDocumentSync = {
    change = 2,
    openClose = true
  },
  typeDefinitionProvider = true,
  workspace = {
    workspaceFolders = {
      changeNotifications = true,
      supported = true
    }
  },
  workspaceSymbolProvider = true
}

