import { Globe, Package, Terminal, Cpu, HardDrive, Variable, CheckCircle2, AlertTriangle, XCircle } from 'lucide-react';
import { Modal, StatusDot, Alert } from '../ui';
import type { EnvironmentDetection } from '../../types';

interface EnvironmentDetectionModalProps {
  detection: EnvironmentDetection;
  environmentName: string;
  isOpen: boolean;
  onClose: () => void;
}

const statusBarColors: Record<EnvironmentDetection['status'], string> = {
  success: 'bg-emerald-500',
  partial: 'bg-amber-500',
  failed: 'bg-red-500',
};

const statusBarTextColors: Record<EnvironmentDetection['status'], string> = {
  success: 'text-emerald-600',
  partial: 'text-amber-600',
  failed: 'text-red-600',
};

const statusBarBgColors: Record<EnvironmentDetection['status'], string> = {
  success: 'bg-emerald-50',
  partial: 'bg-amber-50',
  failed: 'bg-red-50',
};

const statusBarLabels: Record<EnvironmentDetection['status'], string> = {
  success: '探测成功',
  partial: '部分成功',
  failed: '探测失败',
};

function ToolStatusRow({ label, tool }: { label: string; tool: EnvironmentDetection['python'] }) {
  return (
    <div className="flex items-center justify-between py-1">
      <span className="text-sm text-[var(--text-secondary)]">{label}</span>
      <span className="inline-flex items-center gap-1.5 text-sm text-[var(--text)]">
        <StatusDot status={tool.available ? 'success' : 'error'} />
        <span>{tool.available ? '可用' : '不可用'}</span>
        {tool.version ? (
          <code className="rounded bg-[var(--bg-tertiary)] px-1.5 py-0.5 text-xs">{tool.version}</code>
        ) : null}
      </span>
    </div>
  );
}

function InfoRow({ label, value }: { label: string; value: string | number | null }) {
  return (
    <div className="flex items-center justify-between py-1">
      <span className="text-sm text-[var(--text-secondary)]">{label}</span>
      <span className="text-sm text-[var(--text)]">{value ?? '—'}</span>
    </div>
  );
}

function GroupCard({
  icon,
  title,
  children,
}: {
  icon: React.ReactNode;
  title: string;
  children: React.ReactNode;
}) {
  return (
    <div className="rounded-xl border border-[var(--border)] bg-[var(--surface)] p-4">
      <div className="mb-3 flex items-center gap-2">
        <span className="text-[var(--text-secondary)]">{icon}</span>
        <span className="text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)]">
          {title}
        </span>
      </div>
      <div className="space-y-0.5">{children}</div>
    </div>
  );
}

export default function EnvironmentDetectionModal({
  detection,
  environmentName,
  isOpen,
  onClose,
}: EnvironmentDetectionModalProps) {
  const statusColor = statusBarColors[detection.status];
  const statusTextColor = statusBarTextColors[detection.status];
  const statusBgColor = statusBarBgColors[detection.status];
  const statusLabel = statusBarLabels[detection.status];

  const StatusIcon = detection.status === 'success' ? CheckCircle2 : detection.status === 'partial' ? AlertTriangle : XCircle;

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={`${environmentName} · 环境探测结果`}
      size="xl"
    >
      <div className="space-y-4">
        {/* Status bar */}
        <div className={`flex items-center gap-3 rounded-lg ${statusBgColor} p-3`}>
          <div className={`h-1.5 w-1.5 rounded-full ${statusColor}`} />
          <StatusIcon size={18} className={statusTextColor} />
          <span className={`text-sm font-medium ${statusTextColor}`}>{statusLabel}</span>
          {detection.summary ? (
            <span className="text-sm text-[var(--text-secondary)]">{detection.summary}</span>
          ) : null}
        </div>

        {/* Group cards */}
        <div className="grid gap-4 sm:grid-cols-2">
          {/* 基本信息 */}
          <GroupCard icon={<Globe size={16} />} title="基本信息">
            <InfoRow label="SSH 状态" value={detection.ssh_ok ? '正常' : '失败'} />
            <InfoRow label="主机名" value={detection.hostname} />
            <InfoRow label="操作系统" value={detection.os_info} />
            <InfoRow label="架构" value={detection.arch} />
            <InfoRow
              label="工作目录"
              value={detection.workdir_exists === null ? null : detection.workdir_exists ? '存在' : '不存在'}
            />
          </GroupCard>

          {/* Python 工具链 */}
          <GroupCard icon={<Package size={16} />} title="Python 工具链">
            <ToolStatusRow label="Python" tool={detection.python} />
            <ToolStatusRow label="Conda" tool={detection.conda} />
            <ToolStatusRow label="uv" tool={detection.uv} />
            <ToolStatusRow label="pixi" tool={detection.pixi} />
          </GroupCard>

          {/* 开发工具 */}
          <GroupCard icon={<Terminal size={16} />} title="开发工具">
            <ToolStatusRow label="Code Server" tool={detection.code_server} />
            <ToolStatusRow label="Claude CLI" tool={detection.claude_cli} />
          </GroupCard>

          {/* AI/ML 环境 */}
          <GroupCard icon={<Cpu size={16} />} title="AI/ML 环境">
            <ToolStatusRow label="PyTorch" tool={detection.torch} />
            <ToolStatusRow label="CUDA" tool={detection.cuda} />
          </GroupCard>

          {/* GPU 信息 */}
          <GroupCard icon={<HardDrive size={16} />} title="GPU 信息">
            <InfoRow label="GPU 数量" value={detection.gpu_count} />
            <InfoRow
              label="GPU 型号"
              value={detection.gpu_models.length > 0 ? detection.gpu_models.join(', ') : '无'}
            />
          </GroupCard>

          {/* 环境变量 */}
          <GroupCard icon={<Variable size={16} />} title="环境变量">
            <div className="flex items-center justify-between py-1">
              <span className="text-sm text-[var(--text-secondary)]">Anthropic 环境</span>
              <span className="inline-flex items-center gap-1.5 text-sm text-[var(--text)]">
                <StatusDot
                  status={
                    detection.anthropic_env === 'present'
                      ? 'success'
                      : detection.anthropic_env === 'missing'
                        ? 'error'
                        : 'idle'
                  }
                />
                <span>
                  {detection.anthropic_env === 'present'
                    ? '已配置'
                    : detection.anthropic_env === 'missing'
                      ? '未配置'
                      : '未知'}
                </span>
              </span>
            </div>
          </GroupCard>
        </div>

        {/* Errors */}
        {detection.errors.length > 0 ? (
          <div className="space-y-2">
            {detection.errors.map((error, index) => (
              <Alert key={`error-${index}`} variant="error">
                {error}
              </Alert>
            ))}
          </div>
        ) : null}

        {/* Warnings */}
        {detection.warnings.length > 0 ? (
          <div className="space-y-2">
            {detection.warnings.map((warning, index) => (
              <Alert key={`warning-${index}`} variant="warning">
                {warning}
              </Alert>
            ))}
          </div>
        ) : null}
      </div>
    </Modal>
  );
}
