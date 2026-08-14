# qmsWrapper module registry

The authoritative list of module names, taken from the *Validation Test Matrix*
workbook. **Use these names exactly.** A module named loosely fragments the
matrix: a tester filtering on `Training` misses rows filed under
"Training Records", and one module ends up described by two sheets.

- **Module** is what goes in the `Module / Suite` column and in the spec's `module` field.
- **Prefix** is the Test ID prefix for that module's rows (`TRAIN-01`, `TRAIN-02`, …).
- **Filename token** is the `<Module>` part of the house filename convention
  `qmsWrapper_<Module>_<YYYY-MM-DD>_<HHMM>_v<N>`.

Two modules are split across several prefixes by sub-area — say which one you
mean rather than picking the first.

| Module | Prefix | Filename token |
|---|---|---|
| AI Agent Studio (Backend, feature-flagged) | `AISTUDIO` | `AIAgentStudioBackend` |
| Approvals (Global) | `APPR` | `Approvals` |
| Audit Trail | `AUDIT` | `AuditTrail` |
| Authentication & Access | `AUTH` | `AuthenticationAccess` |
| Backend Auth & Access | `BAUTH` | `BackendAuthAccess` |
| Backend Dashboard | `BDASH` | `BackendDashboard` |
| Calendar & To-dos | `CAL / TODO` | `CalendarToDos` |
| Capabilities / Modules (Backend) | `CAP` | `CapabilitiesModulesBackend` |
| Change Management | `CHG` | `ChangeManagement` |
| Conversations / Chat | `CONV` | `ConversationsChat` |
| Dashboard | `DASH` | `Dashboard` |
| Data Recovery Console (Backend) | `RECOV` | `DataRecoveryConsoleBackend` |
| Desktop App | `DESKTOP` | `DesktopApp` |
| EUDAMED | `EUDA` | `EUDAMED` |
| Entity Pickers (Backend) | `PICK` | `EntityPickersBackend` |
| Feedback | `FDBK` | `Feedback` |
| Form Builder | `FORM` | `FormBuilder` |
| Gap Analysis | `GAP` | `GapAnalysis` |
| Global Search | `SRCH` | `GlobalSearch` |
| Issues / Tasks | `ISSUE` | `IssuesTasks` |
| Management Review | `MGMTAUD` | `ManagementReview` |
| Manual Master Templates (Backend) | `MTMPL` | `ManualMasterTemplatesBackend` |
| Manual Vocabulary (Backend) | `MVOC` | `ManualVocabularyBackend` |
| Market/Technical File (MTF) | `MTF` | `MarketTechnicalFile` |
| Migration Manifests (Backend) | `MANIFEST` | `MigrationManifestsBackend` |
| Migration Tools (Backend) | `BMIG` | `MigrationToolsBackend` |
| Migration Wizards (Frontend) | `MIGFE` | `MigrationWizards` |
| Notifications | `NOTIF` | `Notifications` |
| Ops Consoles (Backend) | `CACHE / JOBS / EMAIL / PERF / AIPERF` | `OpsConsolesBackend` |
| Org Troubleshooting (Backend) | `OSUPP` | `OrgTroubleshootingBackend` |
| Organizations (Backend) | `ORG` | `OrganizationsBackend` |
| Process Builder | `PROC` | `ProcessBuilder` |
| Project Administration | `PADM` | `ProjectAdministration` |
| Projects | `PROJ` | `Projects` |
| QMS Manual | `MAN` | `QMSManual` |
| Record Retention | `RET` | `RecordRetention` |
| Reports | `RPT` | `Reports` |
| Risk Management | `RISK` | `RiskManagement` |
| Settings & Administration (Org-Wide) | `SET` | `SettingsAdministration` |
| Start Launcher | `START` | `StartLauncher` |
| Storage / Document Management | `STOR` | `StorageDocumentManagement` |
| Stuck Work Rescue Console (Backend) | `STUCK` | `StuckWorkRescueConsoleBackend` |
| Subscription Packages (Backend) | `PKG` | `SubscriptionPackagesBackend` |
| Subscriptions (Backend) | `SUB` | `SubscriptionsBackend` |
| Supplier Management | `SUPP` | `SupplierManagement` |
| Support Consoles (Backend) | `USUPP` | `SupportConsolesBackend` |
| System Setup Wizard | `WIZSYS` | `SystemSetupWizard` |
| Tags | `TAG` | `Tags` |
| Technical Files | `TECHF` | `TechnicalFiles` |
| Traceability Matrix | `TRACE` | `TraceabilityMatrix` |
| Training | `TRAIN` | `Training` |
| User Deletion Wizard | `UDEL` | `UserDeletionWizard` |
| Users (Backend) | `USR` | `UsersBackend` |
| Vigilance | `VIG` | `Vigilance` |
| WrapperApp Releases (Backend) | `REL` | `WrapperAppReleasesBackend` |

## Renamed modules

These were called something else until 2026-08-10. The old names are dead — the
builder rewrites them, but do not write them yourself.

| Old name | Use instead |
|---|---|
| Form Editor | **Form Builder** |
| Forms (Builder & Submissions) | **Form Builder** |
| Process Editor | **Process Builder** |
| Process / Workflow Engine | **Process Builder** |

## If the module is not listed

Stop and ask. A module missing from this table is either named differently in
the product, or genuinely new — and a genuinely new one needs a prefix assigning
and this table updating, not a guess. Never invent a name to make a document
build.

