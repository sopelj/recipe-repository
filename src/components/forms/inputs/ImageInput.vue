<script setup lang="ts">
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";

const model = defineModel<string | null>();

const props = withDefaults(
  defineProps<{
    id: string;
    label?: string;
    alt?: string;
    errors?: string[] | string;
  }>(),
  {
    label: undefined,
    alt: "",
    errors: () => [],
  },
);

const { t } = useI18n();
const errorList = computed((): string[] => (Array.isArray(props.errors) ? props.errors : [props.errors]));

const fileInput = ref<HTMLInputElement | null>(null);

const triggerUpload = () => {
  fileInput.value?.click();
};

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  const file = target.files?.[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      model.value = e.target?.result as string;
    };
    reader.readAsDataURL(file);
  }
};

const removeImage = () => {
  model.value = null;
  if (fileInput.value) {
    fileInput.value.value = "";
  }
};
</script>

<template>
  <div class="w-full flex flex-col gap-2">
    <label
      v-if="label"
      class="label-text"
      :for="id"
    >
      {{ label }}
    </label>

    <div
      class="relative group w-full aspect-square border-2 border-dashed border-slate-300 dark:border-gray-600 rounded-lg overflow-hidden flex items-center justify-center bg-slate-50 dark:bg-gray-800"
    >
      <img
        v-if="model"
        :src="model"
        :alt="alt"
        loading="lazy"
        class="h-full w-full object-cover"
      />
      <div
        v-else
        class="flex flex-col items-center justify-center text-slate-400 dark:text-gray-500"
      >
        <i class="icon-[mdi-light--image] text-4xl mb-2" />
        <span class="text-xs px-2 text-center">{{ t("edit.no_image_selected") }}</span>
      </div>

      <div
        class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2"
      >
        <button
          type="button"
          class="btn btn-circle btn-sm btn-primary"
          @click="triggerUpload"
        >
          <i class="icon-[mdi-light--pencil] text-lg" />
        </button>
        <button
          v-if="model"
          type="button"
          class="btn btn-circle btn-sm btn-error"
          @click="removeImage"
        >
          <i class="icon-[mdi-light--delete] text-lg" />
        </button>
      </div>
    </div>

    <input
      :id="id"
      ref="fileInput"
      type="file"
      accept="image/*"
      class="hidden"
      @change="handleFileChange"
    />

    <ul
      v-if="errorList?.length"
      class="text-red-500 text-sm"
    >
      <li
        v-for="(error, i) in errorList"
        :key="i"
      >
        {{ error }}
      </li>
    </ul>
  </div>
</template>
