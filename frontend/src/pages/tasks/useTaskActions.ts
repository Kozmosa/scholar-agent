import { useMutation, useQueryClient } from '@tanstack/react-query';
import { pauseTask, resumeTask, sendTaskPrompt } from '../../api';

export function useTaskActions(taskId: string | null) {
  const queryClient = useQueryClient();

  const pause = useMutation({
    mutationFn: () => pauseTask(taskId!),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['task', taskId] });
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  const resume = useMutation({
    mutationFn: () => resumeTask(taskId!),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['task', taskId] });
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
  });

  const sendPrompt = useMutation({
    mutationFn: (prompt: string) => sendTaskPrompt(taskId!, prompt),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['task', taskId] });
      queryClient.invalidateQueries({ queryKey: ['task-messages', taskId] });
    },
  });

  return {
    pause: () => taskId && pause.mutate(),
    resume: () => taskId && resume.mutate(),
    sendPrompt: (prompt: string) => taskId && sendPrompt.mutate(prompt),
    isPending: pause.isPending || resume.isPending || sendPrompt.isPending,
  };
}
