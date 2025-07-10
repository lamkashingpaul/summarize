"use client";

import { AlertFailure } from "@/components/ui/alert-failure";
import { AlertSuccess } from "@/components/ui/alert-success";
import { ButtonWithLoading } from "@/components/ui/button-with-loading";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { InputWithAnEye } from "@/components/ui/input-with-an-eye";
import { useResetPassword } from "@/features/auth/api/use-reset-password";
import { resetPasswordSchema } from "@/features/auth/schemas";
import { formatErrorMessage } from "@/lib/utils";
import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect, useMemo } from "react";
import { SubmitHandler, useForm } from "react-hook-form";
import { z } from "zod";

type ResetPasswordFormProps = {
  token: string;
};

type ResetPasswordFormInput = z.input<typeof resetPasswordSchema>;
type ResetPasswordFormOutput = z.output<typeof resetPasswordSchema>;

export const ResetPasswordForm = (props: ResetPasswordFormProps) => {
  const { token } = props;

  const {
    mutateAsync: resetPassword,
    data: resetPasswordData,
    isPending: isResetPasswordPending,
  } = useResetPassword();

  const form = useForm({
    defaultValues: useMemo(
      () => resetPasswordFormDefaultValues(token),
      [token],
    ),
    resolver: zodResolver(resetPasswordSchema),
    disabled: isResetPasswordPending,
  });

  const {
    handleSubmit,
    control,
    setError,
    reset,
    formState: { errors, isSubmitSuccessful },
  } = form;

  const onSubmit: SubmitHandler<ResetPasswordFormOutput> = async (data) => {
    try {
      await resetPassword(data);
    } catch (error) {
      const errorMessage = formatErrorMessage(error);
      setError("root.serverError", { type: "server", message: errorMessage });
    }
  };

  useEffect(() => {
    if (isSubmitSuccessful) {
      reset();
    }
  }, [isSubmitSuccessful, reset]);

  return (
    <Form {...form}>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {resetPasswordData?.detail ? (
          <AlertSuccess
            title="Password Reset Successful"
            description={`${resetPasswordData.detail} You can now log in with your new password.`}
          />
        ) : null}

        {errors?.root?.serverError?.type === "server" ? (
          <AlertFailure
            title="Reset Password Failed"
            description={errors.root.serverError.message}
          />
        ) : null}

        <FormField
          control={control}
          name="newPassword"
          render={({ field }) => (
            <FormItem>
              <FormLabel>New Password</FormLabel>
              <FormControl>
                <InputWithAnEye placeholder="New Password" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={control}
          name="confirmNewPassword"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Confirm New Password</FormLabel>
              <FormControl>
                <InputWithAnEye placeholder="Confirm New Password" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <ButtonWithLoading
          type="submit"
          className="w-full"
          isLoading={isResetPasswordPending}
        >
          Update Password
        </ButtonWithLoading>
      </form>
    </Form>
  );
};

const resetPasswordFormDefaultValues = (
  token: string,
): ResetPasswordFormInput => ({
  token,
  newPassword: "",
  confirmNewPassword: "",
});
