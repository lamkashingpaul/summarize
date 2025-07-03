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
import { Input } from "@/components/ui/input";
import { useSendResetEmail } from "@/features/auth/api/use-send-reset-email";
import { forgotPasswordSchema } from "@/features/auth/schemas";
import { formatErrorMessage } from "@/lib/utils";
import { zodResolver } from "@hookform/resolvers/zod";
import { useEffect } from "react";
import { SubmitHandler, useForm } from "react-hook-form";
import { z } from "zod/v4";

type ForgotPasswordFormInput = z.input<typeof forgotPasswordSchema>;
type ForgotPasswordFormOutput = z.output<typeof forgotPasswordSchema>;

export const ForgotPasswordForm = () => {
  const {
    mutateAsync: sendResetEmail,
    data: sendResetEmailData,
    isPending: isSendResetEmailPending,
  } = useSendResetEmail();

  const form = useForm({
    defaultValues: forgotPasswordFormDefaultValues,
    resolver: zodResolver(forgotPasswordSchema),
    disabled: isSendResetEmailPending,
  });

  const {
    handleSubmit,
    control,
    setError,
    reset,
    formState: { errors, isSubmitSuccessful },
  } = form;

  const onSubmit: SubmitHandler<ForgotPasswordFormOutput> = async (data) => {
    try {
      await sendResetEmail(data);
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
        {sendResetEmailData?.detail ? (
          <AlertSuccess
            title="Email Sent"
            description={`${sendResetEmailData.detail} Please check your email for the reset link.`}
          />
        ) : null}

        {errors?.root?.serverError?.type === "server" ? (
          <AlertFailure
            title="Error"
            description={errors.root.serverError.message}
          />
        ) : null}

        <FormField
          control={control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="john.doe@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <ButtonWithLoading
          type="submit"
          className="w-full"
          isLoading={isSendResetEmailPending}
        >
          Send Reset Email
        </ButtonWithLoading>
      </form>
    </Form>
  );
};

const forgotPasswordFormDefaultValues = {
  email: "",
} satisfies ForgotPasswordFormInput;
