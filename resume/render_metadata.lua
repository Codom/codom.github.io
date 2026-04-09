local function process_list(list)
  if not list or list.t ~= 'MetaList' then return list end
  local new_list = {}
  for i, v in ipairs(list) do
    if v.t == 'MetaInlines' then
      table.insert(new_list, v)
    elseif v.t == 'MetaString' or type(v) == 'string' then
      local str = (v.t == 'MetaString' and v.text) or v
      local doc = pandoc.read(str, 'markdown')
      local inlines = pandoc.utils.blocks_to_inlines(doc.blocks)
      table.insert(new_list, pandoc.MetaInlines(inlines))
    else
      table.insert(new_list, v)
    end
  end
  return pandoc.MetaList(new_list)
end

local function process_inlines(v)
  if not v then return v end
  if v.t == 'MetaInlines' then return v end
  local str = pandoc.utils.stringify(v)
  local doc = pandoc.read(str, 'markdown')
  local inlines = pandoc.utils.blocks_to_inlines(doc.blocks)
  return pandoc.MetaInlines(inlines)
end

function Meta(meta)
  if meta['left-column'] then
    meta['left-column'] = process_list(meta['left-column'])
  end
  if meta['right-column'] then
    meta['right-column'] = process_list(meta['right-column'])
  end
  if meta['name'] then
    meta['name'] = process_inlines(meta['name'])
  end
  if meta['subheading'] then
    meta['subheading'] = process_inlines(meta['subheading'])
  end
  return meta
end
